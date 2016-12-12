from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from storesb.settings import EMAIL_HOST_USER

from accounts.tasks import send_email_task
from orders.models import Order

from common.decorators import ajax_required
from common.functions import convert_str_to_int

from .models import Complaint, BlockList


# Create your views here.


@require_POST
@login_required
@ajax_required
def add_complaint(request):
    """
    Add complaint. Requires AJAX post request. Check if author can't write abuse to youself and complains to seller
    (they have same order). And optionally block user. Send email to administrators.
    :param request: HttpRequest (contains 'user_id', 'type', 'text', block).
    :return: JsonResponse
    """
    try:
        to_user = User.objects.get(pk=request.POST['user_id'])
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return JsonResponse({'status': 'error'})
    if request.user != to_user:
        complaint = Complaint()
        complaint.complaint_to = to_user
        complaint.complaint_from = request.user
        complaint.text = request.POST.get('text')
        complaint.complaint_type = request.POST.get('type')
        complaint.save()
        # Add to block list if needed
        blocked = 0
        if 'block' in request.POST and convert_str_to_int(request.POST.get('block')) == 1:
            blocklist = BlockList.objects.get_or_create(owner=request.user)[0]
            blocklist.users.add(to_user)
            blocked = 1
        # Sending email to admins
        subject = _("Complaint from %(user_from)s to %(user_to)s") % {'user_from': request.user.username, 'user_to': to_user}
        body = _("Complaint from %(user_from)s to %(user_to)s.\nReason: %(reason)s\n%(text)s") % {
                'user_from': request.user.username,
                'user_to': to_user,
                'reason': complaint.get_complaint_type_display(),
                'text': complaint.text
        }
        mail_to_users = User.objects.filter(is_staff=True).values_list('email', flat=True)
        mail_to_list = [mail for mail in mail_to_users]
        send_email_task.delay(subject, body, EMAIL_HOST_USER, mail_to_list)
        return JsonResponse({'status': 'ok', 'blocked': blocked})
    return JsonResponse({'status': 'error'})


@require_POST
@login_required
@ajax_required
def remove_from_block(request):
    """
    Unblock user. Requires AJAX post request.
    :param request: HttpRequest (contains 'user_id').
    :return: JsonResponse
    """
    try:
        unblocked_user = User.objects.get(pk=request.POST['user_id'])
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return JsonResponse({'status': 'error'})
    request.user.my_blocklist.users.remove(unblocked_user)
    return JsonResponse({'status': 'ok'})
