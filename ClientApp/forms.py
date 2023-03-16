from django import forms
from VendorApp.models import UpperVendor
from Account.models import User
from .models import ScheduleMeeting, EventPlan, VenueRequired, DecorRequired, CatererRequired, PhotographerRequired
from datetime import timedelta

class ScheduleForm(forms.Form):
    service =forms.CharField(max_length=255,required=True,widget=forms.Textarea)
    client = forms.CharField(max_length=30, required=True)
    date = forms.DateField(required=True)
    time = forms.TimeField(required=True)
    contact_number = forms.CharField(max_length=12, required=True)
    def getVirtualMeeting(self):
        service = self.cleaned_data['service']
        client = self.cleaned_data['client']
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        contact_number = self.cleaned_data['contact_number']
        try:
            if len(contact_number)<10:
                raise forms.ValidationError("Provide a valid address.")
            else:
                up = UpperVendor.objects.get(vendor_name=service)
                user_client = User.objects.get(username=client)
                schedule_meeting = ScheduleMeeting(service=up, client=user_client,mode=False,contact_number=contact_number,date=date,time=time)
                schedule_meeting.save()
        except Exception as e:
            print(e)
        return "Saved"
    
    def getPersonMeeting(self):
        service = self.cleaned_data['service']
        client = self.cleaned_data['client']
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        contact_number = self.cleaned_data['contact_number']
        try:
            if len(contact_number)<10:
                raise forms.ValidationError("Provide a valid address.")
            else:
                up = UpperVendor.objects.get(vendor_name=service)
                user_client = User.objects.get(username=client)
                schedule_meeting = ScheduleMeeting(service=up, client=user_client,mode=True,contact_number=contact_number,date=date,time=time)
                schedule_meeting.save()
        except Exception as e:
            print(e)
        return "Saved"

class DeleteSchedule(forms.Form):
    service = forms.CharField(max_length=50, required=True)
    client = forms.CharField(max_length=50, required=True)
    def deletingSchedule(self):
        service = self.cleaned_data['service']
        client = self.cleaned_data['client']
        try:
            user_client = User.objects.get(username=client)
            up = UpperVendor.objects.get(vendor_name=service)
            schedule_meeting = ScheduleMeeting.objects.get(service=up, client=user_client)
            schedule_meeting.delete()
        except Exception as e:
            print("Deletion of meeting was not successfully: ",e)
        
        return "deleted"


class CreateEventForm(forms.Form):
    user = forms.CharField(max_length=40)
    theme = forms.CharField(max_length=40)
    event_name = forms.CharField(max_length=40)
    venue_require = forms.BooleanField(required=False)
    caterer_require = forms.BooleanField(required=False)
    decor_require = forms.BooleanField(required=False)
    photographer_require = forms.BooleanField(required=False)
    deadline = forms.DateField(required=True)
    budget = forms.CharField(max_length=1)

    def createdEvent(self):

        user = self.cleaned_data['user']
        theme = self.cleaned_data['theme']
        event_name = self.cleaned_data['event_name']
        venue_require = self.cleaned_data['venue_require']
        caterer_require = self.cleaned_data['caterer_require']
        decor_require = self.cleaned_data['decor_require']
        photographer_require = self.cleaned_data['photographer_require']
        deadline = self.cleaned_data['deadline']
        budget = self.cleaned_data['budget']
        field_list = [user, theme, event_name,deadline,budget]
        try:
            client_name= User.objects.get(username=user)
            if None in field_list:
                raise forms.ValidationError("Fields cannot be empty.")
            event_plan = EventPlan(
                user=client_name,
                theme=theme,
                event_name=event_name,
                venue_require=venue_require,
                caterer_require=caterer_require,
                decor_require=decor_require,
                photographer_require=photographer_require,
                deadline=deadline,
            )
            if budget == '1':
                event_plan.min_budget = 30000
                event_plan.max_budget = 60000
                event_plan.save()
            elif budget == '2':
                event_plan.min_budget = 60000
                event_plan.max_budget = 90000
                event_plan.save()
            elif budget == '3':
                event_plan.min_budget = 90000
                event_plan.max_budget = 120000
                event_plan.save()
            elif budget == '4':
                event_plan.min_budget = 120000
                event_plan.max_budget = 150000
                event_plan.save()
            elif budget == '5':
                event_plan.min_budget = 150000
                event_plan.max_budget = 250000
                event_plan.save()
        except Exception as e:
            print(e)
        return "saved"


class EventRequire(forms.Form):
    type = forms.CharField(max_length=25)
    service_name = forms.CharField(max_length=25)
    event_plan = forms.CharField(max_length=30)

    def eventRequired(self):
        type = self.cleaned_data['type']
        event_plan = self.cleaned_data['event_plan']
        service_name = self.cleaned_data['service_name']
        try:
            if type == 'VENUE':
                event_name = EventPlan.objects.get(event_name=event_plan)
                vendor_name = UpperVendor.objects.get(vendor_name=service_name)
                venue_required = VenueRequired(event_plan=event_name, venue=vendor_name)
                venue_required.save()
            elif type == 'CATERER':
                event_name = EventPlan.objects.get(event_name=event_plan)
                vendor_name = UpperVendor.objects.get(vendor_name=service_name)
                caterer_required = CatererRequired(event_plan=event_name, venue=vendor_name)
                caterer_required.save()
            elif type == 'DECOR':
                event_name = EventPlan.objects.get(event_name=event_plan)
                vendor_name = UpperVendor.objects.get(vendor_name=service_name)
                decor_required = DecorRequired(event_plan=event_name, venue=vendor_name)
                decor_required.save()
            elif type == 'PHOTOGRAPHER':
                event_name = EventPlan.objects.get(event_name=event_plan)
                vendor_name = UpperVendor.objects.get(vendor_name=service_name)
                photographer_required = PhotographerRequired(event_plan=event_name, venue=vendor_name)
                photographer_required.save()
        except Exception as e:
            print(e)
        return "saved"