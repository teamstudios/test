from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Thread(models.Model):
    """
    Thread model. Contains all users in chat.
    """
    participants = models.ManyToManyField(User, verbose_name=_("Users"), related_name='threads')
    last_message = models.DateTimeField(null=True, blank=True, db_index=True)
    has_unread = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('chat:show_thread', args=[self.id])

    def get_message_count(self):
        return Message.objects.filter(thread=self).count()

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ('-last_message',)


class Message(models.Model):
    """
    Message model.
    """
    sender = models.ForeignKey(User, verbose_name=_("Sender"), related_name='my_messages')
    thread = models.ForeignKey(Thread, verbose_name=_("Thread"), related_name='messages')
    text = models.TextField(verbose_name=_("Message"))
    datetime = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Date and time"))


def update_last_message_datetime(sender, instance, created, **kwargs):
    """
    Update Thread's last_message field when new message sent
    """
    if not created:
        return
    Thread.objects.filter(id=instance.thread.id).update(last_message=instance.datetime, has_unread=True)


post_save.connect(update_last_message_datetime, sender=Message)
