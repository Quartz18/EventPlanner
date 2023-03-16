from django.shortcuts import render, redirect
from Account.decorators import authenticated_user
from VendorApp.models import UpperVendor
from VendorApp.files import FilesAndImages
from Account.models import User
from .models import ScheduleMeeting, EventPlan, VenueRequired, DecorRequired, CatererRequired, PhotographerRequired
from .forms import ScheduleForm, DeleteSchedule, CreateEventForm, EventRequire
from .files import ClientRetrieval
from django.http import HttpRequest, JsonResponse, Http404, HttpResponse
import os
from django.conf import settings

# Create your views here.

def convertIntoJSON(my_vendor):
    vendor_list = []
    checkimage = FilesAndImages()
    for vendor in my_vendor:
        data1 = {
            'id': vendor.pk,
            'name': str(vendor.venue.vendor_name),
            'type': vendor.venue.type,
        }
        vendor_list.append(data1)
    return vendor_list

@authenticated_user
def user_home_view(request, *args, **kwargs):
    print("Type",request.user.type)
    return render(request,"client/home_view.html",context={'username':request.user}, status=200)

@authenticated_user
def category_view(request,category, *args, **kwargs):
    data = {
        'username': request.user
    }
    if(category == 'venue'):
        return render(request,"client/category_venue.html",context=data, status=200)
    elif(category == 'caterer'):
        return render(request,"client/category_caterer.html",context=data, status=200)
    elif(category == 'decor'):
        return render(request,"client/category_decor.html",context=data, status=200)
    elif(category == 'photographer'):
        return render(request,"client/category_photographer.html",context=data, status=200)
    else:
        return render(request,"client/category_view.html",context=data, status=200)
    return render(request,"client/category_view.html",context=data, status=200)

@authenticated_user
def vendor_detail(request,vendor_name, *args, **kwargs):
    data = {}
    my_vendor = None
    client_username = User.objects.get(username=request.user)
    checkimage = FilesAndImages()
    files_of_client = ClientRetrieval()
    try:
        my_vendor = UpperVendor.objects.get(vendor_name=vendor_name)
        data = {
            'username':request.user,
            'response': my_vendor,
        }
    except Exception as e:
        print("Private Profile:", e)
    else:
        data = checkimage.getFiles(my_vendor, data)
        data = checkimage.getPolicyandTime(my_vendor.type,my_vendor,data)
        data = checkimage.uploadImage(my_vendor, data)
        data = checkimage.getPartArea(my_vendor.type, my_vendor, data)
        data = checkimage.getFoodPackage(my_vendor.type, my_vendor, data)
        data = checkimage.getDecorPackage(my_vendor.type, my_vendor, data)
        data = files_of_client.getScheduleSpecific(my_vendor,client_username,data)
    return render(request,"client/details.html",context=data, status=200)

def schedule_meeting(request, *args, **kwargs):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        
        if request.POST.get("mode"):
            if form.is_valid():
                d1 = form.getPersonMeeting()
                obj2 = request.POST.get("service")
                return redirect(f"/u/details/{obj2}/")
        elif request.POST.get("no_mode"):
            if form.is_valid():
                d1 = form.getVirtualMeeting()
                obj2 = request.POST.get("service")
                return redirect(f"/u/details/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/u/")

def cancel_schedule(request, *args, **kwargs):
    if request.method == 'POST':
        form = DeleteSchedule(request.POST)
        if form.is_valid():
            d1 = form.deletingSchedule()
            obj2 = request.POST.get("service")
            return redirect(f"/u/details/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/u/")

@authenticated_user
def profile_view(request, *args, **kwargs):
    data = {
        'username' : request.user
    }
    return render(request, "client/profile_view.html",context=data, status=200)


def create_event(request, *args, **kwargs):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            d1 = form.createdEvent()
            return redirect(f"/u/profile/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/u/")


def schedule_list(request, *args, **kwargs):
    client_name = User.objects.get(username=request.user)
    confirm_schedule_list =[]; pending_schedule_list =[]
    checkimage = FilesAndImages()
    try:
        schedule = ScheduleMeeting.objects.filter(client=client_name)
        if schedule.exists():
            for scheduling in schedule:
                    data1 = {'name':scheduling.service.vendor_name,
                    'address':scheduling.service.vendor_address,
                    'category':scheduling.service.type,
                    'confirm_schedule': scheduling.confirm_schedule,
                    'client': scheduling.client.username,
                    's_date': scheduling.date.strftime("%d %b, %Y"),
                    's_time': scheduling.time.strftime("%I:%M %P"),
                    'mode': scheduling.mode,
                    'contact_number': scheduling.contact_number}
                    data1 = checkimage.uploadImage(scheduling.service, data1)
                    if(scheduling.confirm_schedule==True):
                        confirm_schedule_list.append(data1)
                    else:
                        pending_schedule_list.append(data1)
        data = {
            'confirm_schedule_list' : confirm_schedule_list,
            'pending_schedule_list' : pending_schedule_list,
        }
    except Exception as e:
        print("Vendor: ", str(e))
    return JsonResponse(data)

def event_list(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    data = {}
    vendor_list = []
    try:
        username = User.objects.get(username=request.user)
        all_my_events = username.eventplan_set.all()
        for x in all_my_events:
            data1 = {'name':x.event_name, 'theme':x.theme, 'deadline':x.deadline, 'min_budget':x.min_budget, 'max_budget':x.max_budget}
            vendor_list.append(data1)
        data = {
            'vendor_list' : vendor_list
        }
    except Exception as e:
        print("Vendor: ", str(e))

    return JsonResponse(data)

@authenticated_user
def event_details(request, event_name,*args, **kwargs):
    data = {}
    vendor_list = []
    try:
        event_plan = EventPlan.objects.get(event_name=event_name)
        data = {
            'username': request.user
        }
    except Exception as e:
        print(e)
    return render(request, "client/event_details.html", context=data, status=200)

def major_event_details(request, event_name,*args, **kwargs):
    data = {}
    checkimage = FilesAndImages()
    vendor_list = []
    try:
        event_plan = EventPlan.objects.get(event_name=event_name)
        venue_required = VenueRequired.objects.filter(event_plan=event_plan)
        caterer_required = CatererRequired.objects.filter(event_plan=event_plan)
        decor_required = DecorRequired.objects.filter(event_plan=event_plan)
        photographer_required = PhotographerRequired.objects.filter(event_plan=event_plan)
        vendor_list = [venue_required, venue_required, decor_required, photographer_required]
        print(venue_required[0].venue.vendor_address)
        if(venue_required.exists):
            data1 = {
                'name': venue_required[0].venue.vendor_name,
                'category': venue_required[0].venue.type,
                'address' : venue_required[0].venue.vendor_address
            }
            data1 = checkimage.uploadImage(venue_required[0].venue, data1)
            data['my_vendor'] = [data1]
        if(caterer_required):
            data1 = {
                'name': caterer_required[0].caterer.vendor_name,
                'category': caterer_required[0].caterer.type,
                'address' : caterer_required[0].caterer.vendor_address
            }
            data1 = checkimage.uploadImage(caterer_required[0].caterer, data1)
            data['my_vendor'] = [data1]
        if(decor_required):
            data1 = {
                'name': decor_required[0].decor.vendor_name,
                'category': decor_required[0].decor.type,
                'address' : decor_required[0].decor.vendor_address
            }
            data1 = checkimage.uploadImage(decor_required[0].decor, data1)
            data['my_vendor'] = [data1]
        if(photographer_required):
            data1 = {
                'name': photographer_required[0].photographer.vendor_name,
                'category': photographer_required[0].photographer.type,
                'address' : photographer_required[0].photographer.vendor_address
            }
            data1 = checkimage.uploadImage(photographer_required[0].photographer, data1)
            data['my_vendor'] = [data1]
        else:
            data = {
                'my_vendor': [],
                'my_caterer': [],
                'my_decor': [],
                'my_photographer': []
            }
    except Exception as e:
        print(e)
    return JsonResponse(data)


def eventRequire(request,*args, **kwargs):
    if request.method == 'POST':
        form = EventRequire(request.POST)
        if form.is_valid():
            d1 = form.eventRequired()
            obj2 = request.POST.get("service_name")
            return redirect(f"/u/details/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/u/")



        