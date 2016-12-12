from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from parler.models import TranslatedFields, TranslatableModel
from tinymce.models import HTMLField

from main.models import BaseModel

# Create your models here.


class Page(BaseModel, TranslatableModel):
    """
    Page model.
    """
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Title')),
        content=HTMLField(verbose_name=_('Content')))
    url = models.SlugField(verbose_name=_('URL'), unique=True)
    ceo_keywords = models.TextField(verbose_name='META keywords', null=True, blank=True)
    ceo_description = models.TextField(verbose_name='META description', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:page_view', args=[self.url])

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ("created",)

