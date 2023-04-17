
from django import forms
from django.contrib.auth.models import User
# from . import models
from django.db import models



class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)