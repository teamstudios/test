from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.conf import settings

from common.decorators import ajax_required
from main.forms import SearchForm
from .models import Thread, Message
from .functions import check_user_in_blocklist, send_message_helper

# Create your views here.


@login_required
def show_threads_list(request):
    """
    Show thread list
    :param request:
    :return:
    """
    threads = Thread.objects.filter(participants=request.user)
    if threads:
        for thread in threads:
            try:
                thread.partner = thread.participants.exclude(id=request.user.id)[0]
            except IndexError:
                thread.partner = None
    form = SearchForm()
    return render(request, 'threads_list.html', {'threads': threads, 'user': request.user, 'form': form})


@login_required
@require_POST
def send_message(request):
    """
    Send message through form
    :param request:
    :return:
    """
    sender = request.user
    try:
        partner = User.objects.get(username=request.POST['partner'])
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        messages.error(request, _("Your partner doesn't exist or error in username"))
        return render(request, 'error.html')
    if sender == partner:
        messages.error(request, _("You can't send messages to yourself"))
        return render(request, 'error.html')
    # Check that sender is not in block list
    if check_user_in_blocklist(sender, partner):
        messages.error(request, _("Your partner blocked messages from you"))
        return render(request, 'error.html')
    threads = Thread.objects.filter(participants=partner).filter(participants=sender)
    if threads.exists():
        thread = threads[0]
    else:
        thread = Thread()
        thread.save()
        thread.participants.add(sender, partner)
    send_message_helper(thread, request.POST.get('text'), sender)
    return redirect(reverse('chat:show_thread', args=[thread.id]))


@login_required
def show_thread(request, thread_id):
    """
    Show messages thread
    :param request: HttpRequest
    :param thread_id: Thread id
    :return:
    """
    thread = get_object_or_404(Thread, id=thread_id)
    thread.has_unread = False
    thread.save()
    messages = Message.objects.filter(thread=thread).order_by("datetime")
    try:
        partner = thread.participants.exclude(id=request.user.id)[0]
    except IndexError:
        partner = None
    form = SearchForm()
    return render(request, 'thread.html', {'thread': thread, 'messages': messages, 'partner': partner,
                                           'user': request.user, 'form': form})


@csrf_exempt
@require_POST
def send_message_api(request):
    """
    Accept messages from tornado app
    :param request: Retirn JsonResponse
    :return:
    """
    if request.POST['API_KEY'] == settings.MESSAGE_API_KEY:
        try:
            thread = Thread.objects.get(id=request.POST['thread'])
        except (Thread.DoesNotExist, Thread.MultipleObjectsReturned):
            return JsonResponse({'Error': 'Invalid thread id'})
        try:
            sender = User.objects.get(id=request.POST['sender_id'])
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return JsonResponse({'Error': 'Invalid user id', 'thread': thread.id})
        text = request.POST.get('text')
        recipients = thread.participants.exclude(id=sender.id)
        for patner in recipients:
            if check_user_in_blocklist(sender, patner):
                return JsonResponse({'Error': 'Sender in blocklist', 'thread': thread.id})
        message = send_message_helper(thread, text, sender)
        return JsonResponse({'status': 'ok', 'datetime': message.datetime.strftime('%Y-%m-%d %H:%M:%S'),
                             'sender': message.sender.username, 'sender_id': message.sender.id,
                             'text': message.text, 'thread': message.thread.id})
    else:
        return JsonResponse({'Error': 'Invalid API key'})


@require_POST
@ajax_required
def check_username(request):
    """
    Check if users with this symbols exists. If true return first username. Else return error and empty result.
    Call by AJAX check_username script.
    :param request: HttpRequest (Post with 'parther' parameter)
    :return: Json response
    """
    users = User.objects.filter(username__icontains=request.POST.get('partner'))
    if users.count() != 0:
        return JsonResponse({'status': 'ok', 'result': users[0].username})
    else:
        return JsonResponse({'status': 'error', 'result': ''})


@require_POST
@login_required
@ajax_required
def send_message_ajax(request):
    """
    Send message method, which called by AJAX.
    :param request: HttpRequest (AJAX)
    :return: HttpResponse as JSON
    """
    sender = request.user
    try:
        partner = User.objects.get(pk=request.POST['partner'])
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'reason': 'User not found'})
    if sender == partner:
        return JsonResponse({'status': 'error', 'reason': 'Recipient cannot be yourself'})
    # Check that sender is not in block list
    if check_user_in_blocklist(sender, partner):
        return JsonResponse({"status": "error", 'reason': 'You blocked'})
    threads = Thread.objects.filter(participants=partner).filter(participants=sender)
    if threads.exists():
        thread = threads[0]
    else:
        thread = Thread()
        thread.save()
        thread.participants.add(sender, partner)
    send_message_helper(thread, request.POST.get('text'), sender)
    return JsonResponse({'status': 'ok'})
