
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db import transaction
from .models import User,Client, Vendor, VendorMore

class  UserSignUpForm(forms.Form):
    
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_content(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match")
        return username, email, password

    def saveUser(self): 
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = User.objects.create_user(username = username, email = email, password = password,type=User.Types.CLIENT)
        user_group = user.save()
        # group_main = Group.objects.get(name="client")
        # user_group.groups.add(group_main)
        return user

class  VendorSignUpForm(forms.Form):
    
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_content(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match")
        return username, email, password

    def saveVendor(self): 
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        phone = self.cleaned_data.get("phone")
        password = self.cleaned_data.get("password")
        vendor = User.objects.create_user(username = username, email = email, password = password,type=User.Types.VENDOR)
        user_group = vendor.save()
        vendor_user = User.objects.get(username=username)
        # group_main = Group.objects.get(name="vendor")
        # vendor_user.groups.add(group_main)
        vendor_more = VendorMore.objects.create(user=vendor_user, phone=phone)
        return vendor
        