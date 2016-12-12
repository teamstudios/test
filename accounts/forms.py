from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from main.countries_list import COUNTRIES

from .models import UserProfile, SocialNetwork


class UserRegistrationForm(forms.Form):
    """
    User registration form.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': "E-mail"}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Your mobile phone number")}), required=False)
    confirm_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Confirm code")}), required=False)
    accept = forms.BooleanField(required=True, label=_("I agree to the user agreement"))

    def clean_phone(self):
        cd = self.cleaned_data
        phone = cd['phone']
        if phone:
            if len(phone) < 10 or not phone.isdigit():
                raise forms.ValidationError(_("Your phone should be in format 79994567891 or 89994567891"))
        return cd['phone']


class PasswordResetEmailForm(forms.Form):
    """
    Form to enter email for password reset.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': "E-mail"}))


class PasswordResetPhoneForm(forms.Form):
    """
    Form to enter phone for password reset.
    """
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Your mobile phone number")}))

    def clean_phone(self):
        cd = self.cleaned_data
        phone = cd['phone']
        if phone:
            if len(phone) < 10 or not phone.isdigit():
                raise forms.ValidationError(_("Your phone should be in format 79994567891 or 89994567891"))
        return cd['phone']


class PasswordResetConfirmPhoneForm(forms.Form):
    """
    Form to enter sms code for password reset.
    """
    confirm_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Confirm code")}))


class UserEditForm(forms.ModelForm):
    """
    Form to edit user's username and email
    """
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileEditForm(forms.ModelForm):
    """
    Forms to edit user profile
    """
    org_form = forms.ChoiceField(choices=UserProfile.ORG_FORM, widget=forms.RadioSelect())
    sex = forms.ChoiceField(choices=UserProfile.SEX, widget=forms.RadioSelect())
    auto_post_to_networks = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                                           queryset=SocialNetwork.objects.all())

    class Meta:
        model = UserProfile
        exclude = ['user', 'avatar', 'cover' , 'theme', 'status', 'map_link']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 10})
        }


class SetNewPassword(forms.Form):
    """
    Set password form. Used on reset/set first password on activation.
    """
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Password's don't match.")
        # At least MIN_LENGTH long
        if len(cd['password2']) < 8:
            raise forms.ValidationError(_("The new password must be at least %d characters long.") % 8)
        # At least one letter and one non-letter
        first_isalpha = cd['password2'][0].isalpha()
        if all(c.isalpha() == first_isalpha for c in cd['password2']):
            raise forms.ValidationError(_("""
                The new password must contain at least one letter and at least one digit or punctuation character."""))
        return cd['password2']