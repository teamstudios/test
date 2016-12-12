from django import forms
from .models import Good, GoodsProperties
from django.utils.translation import ugettext_lazy as _


class GoodForm(forms.ModelForm):
    """
    Good form
    """
    quantity = forms.CharField(required=False)
    old_price = forms.CharField(required=False)
    new_price = forms.CharField(required=False)
    price = forms.CharField(required=False)
    # min_price = forms.CharField(required=False)
    # reserve_price = forms.CharField(required=False)
    # max_price = forms.CharField(required=False)

    class Meta:
        model = Good
        exclude = ('user', 'is_active', 'users_like', )


class CustomImageUpload(forms.Form):
    """
    Upload images form. Used in add_goods template and view
    """
    image1 = forms.CharField(required=False, widget=forms.HiddenInput())
    image2 = forms.CharField(required=False, widget=forms.HiddenInput())
    image3 = forms.CharField(required=False, widget=forms.HiddenInput())
    image4 = forms.CharField(required=False, widget=forms.HiddenInput())
    image5 = forms.CharField(required=False, widget=forms.HiddenInput())


class GoodPropetiesForm(forms.ModelForm):
    """
    Good properties form
    """
    class Meta:
        model = GoodsProperties
        exclude = ('good',)
