from django import forms
from .models import user_admin, lead_sources, lead_status, create_lead, user_client, Customer
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class lead_sources_form(forms.ModelForm):
    class Meta:
        model = lead_sources
        fields = ('name',)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class lead_status_form(forms.ModelForm):
    class Meta:
        model = lead_status
        fields = ('name', 'background_color', 'text_color')


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class Admin_Profile(forms.ModelForm):
    class Meta:
        model = user_admin
        fields = ('image', 'mobile')


class Client_Profile(forms.ModelForm):
    class Meta:
        model = user_client
        fields = ('image', 'mobile')


# from django.contrib.auth import get_user_model
# User = get_user_model()
# class client_user_form(forms.ModelForm):
#     class Meta:
#         model = user_client
#         fields = ['user', 'mobile', 'image', 'email', 'password']


# class admin_update_form(forms.ModelForm):
#     class Meta:
#         model = (user_admin, User)
#         fields = ('user.username', 'user.email', 'user.password', 'image', 'mobile')


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class create_lead_form(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'cols': 10}))

    class Meta:
        model = create_lead
        fields = ('name', 'query', 'mobile', 'email', 'lead_sour', 'lead_stat', 'lead_assign', 'description')


class update_lead_form_without_status(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'cols': 10}))

    class Meta:
        model = create_lead
        fields = ('name', 'query', 'mobile', 'email', 'lead_sour', 'lead_assign', 'description')


class lead_history_form(forms.ModelForm):
    remark = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 10}))

    class Meta:
        model = create_lead
        fields = ('lead_stat', 'follow_up_date', 'remark',)
        widgets = {
            'follow_up_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # def clean_date(self):
    #     d = self.cleaned_data.get('follow_up_date')
    #     if d < date.today():
    #         raise ValidationError('Follow Up Date Cannot be in the Past')
    #     return d


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
