from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from main.models import BaseModel

from .constants import COMPLAINT_NOT_DEFINED, OWNER_IMPERSONATE, FRAUD, SPAM, ADVERTISE

# Create your models here.


class Complaint(BaseModel):
    """
    Complaint model
    """
    TYPES = (
        (COMPLAINT_NOT_DEFINED, _("Not defined")),
        (OWNER_IMPERSONATE, _("Owner profile is impersonating another")),
        (FRAUD, _("Fraud")),
        (SPAM, _("Spam")),
        (ADVERTISE, _("Advertising page clog up search"))
    )

    complaint_to = models.ForeignKey(User, related_name='to_me_complaints')
    complaint_from = models.ForeignKey(User, related_name='my_complaints')
    text = models.TextField()
    complaint_type = models.SmallIntegerField(choices=TYPES, default=0)

    def __str__(self):
        return "Complaint to {}".format(self.complaint_to.username)

    class Meta:
        ordering = ("-created",)


class BlockList(BaseModel):
    """
    Block list model
    """
    owner = models.OneToOneField(User, related_name="my_blocklist")
    users = models.ManyToManyField(User, related_name='blocked_users')

    def __str__(self):
        return "BlockList of {}".format(self.owner.username)

    class Meta:
        ordering = ("-created",)

