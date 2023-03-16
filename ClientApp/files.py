import os
from django.conf import settings
from django.http import HttpRequest, JsonResponse, Http404
from VendorApp.models import UpperVendor, VendorTiming, VendorPolicy, VenuePolicy, PartArea
from .models import ScheduleMeeting

class ClientRetrieval():

    def __init__(self):
        count = 0
    
    def getScheduleSpecific(self, service, client, data):
        try:
            schedule = ScheduleMeeting.objects.filter(service=service, client=client)
            if schedule.exists():
                data['schedule_specific'] = schedule[0]
        except Exception as e:
            print("Schedule Meeting Specific: ",e)
        return data
    
