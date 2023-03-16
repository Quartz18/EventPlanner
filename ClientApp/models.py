from django.db import models
from Account.models import User
from VendorApp.models import UpperVendor, Venue, Decor, Photographer, Caterer
from django.core.validators import RegexValidator
import datetime

# Create your models here.

class ScheduleMeeting(models.Model):
    service = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.BooleanField(default=False)
    phone_regrex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone No. must be entered in the format +919999999999.")
    contact_number = models.CharField(max_length=12, validators=[phone_regrex])
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    confirm_schedule = models.BooleanField(default=False)


class EventPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=25, default="Corporate")
    event_name = models.CharField(max_length=40)
    venue_require = models.BooleanField(default=True)
    caterer_require = models.BooleanField(default=False)
    decor_require = models.BooleanField(default=False)
    photographer_require = models.BooleanField(default=False)
    deadline = models.DateField(auto_now=False, auto_now_add=False)
    min_budget = models.IntegerField(default=35000)
    max_budget = models.IntegerField(default=100000)


class VenueRequired(models.Model):
    event_plan = models.ForeignKey(EventPlan, on_delete=models.CASCADE)
    venue = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)

class CatererRequired(models.Model):
    event_plan = models.ForeignKey(EventPlan, on_delete=models.CASCADE)
    caterer = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)

class DecorRequired(models.Model):
    event_plan = models.ForeignKey(EventPlan, on_delete=models.CASCADE)
    decor = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)

class PhotographerRequired(models.Model):
    event_plan = models.ForeignKey(EventPlan, on_delete=models.CASCADE)
    photographer = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)