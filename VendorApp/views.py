from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, Http404, HttpResponse
from Account.decorators import unauthenticated_user, authenticated_vendor, authenticated_user
from .forms import (
    VendorForm,
    EditTimeForm,
    EditImageForm,
    EditAddressForm,
    EditContactForm,
    EditPolicyForm,
    EditPartyForm,
    EditFoodForm,
    EditDecorForm,
    EditPhotographerForm,
    EditNameForm,
    EditScheduleForm,
    DeleteService
)
from Account.models import User
from .files import FilesAndImages
from .models import UpperVendor, VendorTiming, VendorImage,VendorDecor, VendorFood, VendorPhotographer
from ClientApp.models import ScheduleMeeting
from datetime import datetime
import os
from django.conf import settings
# Create your views here.


@authenticated_vendor
def vendor_home_view(request, *args, **kwargs):
    return render(request,"vendor/home_view.html",context={'username':request.user}, status=200)

@authenticated_vendor
def profile_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = VendorForm(request.POST,request.FILES)
        try:
            if form.is_valid():
                obj = form.save(commit=False)
                username = User.objects.get(username=request.user)
                obj.user = username
                obj.save()
                f1 = FilesAndImages()
                f1.saveOtherClass(obj.type, obj)
                form = VendorForm()
                return redirect("/Vendor/u/")
            else:
                raise Http404
        except Exception as e:
            print("View: ",e)
    form = VendorForm()
    context={'username':request.user, 'form': form}
    return render(request,"vendor/profile_view.html",context=context, status=200)

def vendor_basic_form_view(request,*args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    data = {}
    try:
        username = User.objects.get(username=request.user)
        all_my_vendors = username.uppervendor_set.all()
        vendor_list =[]
        checkimage = FilesAndImages()
        for x in all_my_vendors:
            data1 = {'name':x.vendor_name, 'address':x.vendor_address, 'category':x.type}
            data1 = checkimage.uploadImage(x, data1)
            vendor_list.append(data1)
        data = {
            'vendor_list' : vendor_list
        }
    except Exception as e:
        print("Vendor: ", str(e))

    return JsonResponse(data)


@authenticated_vendor
def vendor_profile_detail(request,vendor_name, *args, **kwargs):
    data = {}
    my_vendor = None
    checkimage = FilesAndImages()
    try:
        my_vendor = UpperVendor.objects.get(vendor_name=vendor_name)
        username1= str(my_vendor.user.username)
        username2 = str(request.user)
        if (username1 !=username2):
            raise Http404
        data = {
            'username':request.user,
            'response': my_vendor,
        }
    except Exception as e:
        print("Profile:", e)
    else:
        data = checkimage.getFiles(my_vendor, data)
        data = checkimage.getPolicyandTime(my_vendor.type,my_vendor,data)
        data = checkimage.uploadImage(my_vendor, data)
        data = checkimage.getPartArea(my_vendor.type, my_vendor, data)
        data = checkimage.getFoodPackage(my_vendor.type, my_vendor, data)
        data = checkimage.getDecorPackage(my_vendor.type, my_vendor, data)
        data = checkimage.getPhotgrapherPackage(my_vendor.type, my_vendor, data)
        print(data)
    return render(request,"vendor/details.html",context=data, status=200)

def edit_time_form(request,*args, **kwargs):
    if request.method == 'POST':
        form = EditTimeForm(request.POST)
        if form.is_valid():
            d1 = form.checkTime()
            obj2 = form.saveTime()
            print(obj2)
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_image_form(request,*args, **kwargs):
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('vendor_image')
        print(images)
        form = EditImageForm(request.POST, request.FILES)
        if form.is_valid():
            print("Ok 1")
            vendor_name, category = form.checkImage()
            for image in images:
                vendor_photo = VendorImage.objects.create(
                    vendor_name = vendor_name,
                    vendor_image = image,
                    category = category
                )
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_address_form(request,*args, **kwargs):
    if request.method == 'POST':
        form = EditAddressForm(request.POST)
        if form.is_valid():
            d1 = form.updateAddress()
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_contact_form(request,*args, **kwargs):
    if request.method == 'POST':
        form = EditContactForm(request.POST)
        if form.is_valid():
            d1 = form.updateContact()
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_policy_form(request,*args, **kwargs):
    if request.method == 'POST':
        print(request.POST.get("cancellation"))
        form = EditPolicyForm(request.POST)
        if form.is_valid():
            d1 = form.updatePolicy()
            print(d1)
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_party_form(request,*args, **kwargs):
    if request.method == 'POST':
        form = EditPartyForm(request.POST)
        if form.is_valid():
            d1 = form.addPartyArea()
            print(d1)
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_food_form(request,*args, **kwargs):
    if request.method == 'POST':
        form = EditFoodForm(request.POST)
        if form.is_valid():
            d1 = form.addFood()
            print(d1)
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_decor_form(request,*args, **kwargs):
    if request.method == 'POST':
        form = EditDecorForm(request.POST)
        if form.is_valid():
            d1 = form.addDecor()
            print(d1)
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_photographer_form(request,*args, **kwargs):
    if request.method == 'POST':
        form = EditPhotographerForm(request.POST)
        print(request.POST)
        if form.is_valid():
            d1 = form.addPhotograher()
            print(d1)
            obj2 = request.POST.get("vendor_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")

def edit_name_form(request,*args, **kwargs):
    if request.method == 'POST':
        form = EditNameForm(request.POST)
        if form.is_valid():
            d1 = form.updateName()
            print(d1)
            obj2 = request.POST.get("service_name")
            return redirect(f"/Vendor/vendor/{obj2}/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/u/")


@authenticated_vendor
def category_view(request,category, *args, **kwargs):
    context = {
        'username': request.user
    }
    if(category == 'venue'):
        return render(request,"vendor/category_venue.html",context=context, status=200)
    elif(category == 'caterer'):
        return render(request,"vendor/category_caterer.html",context=context, status=200)
    elif(category == 'decor'):
        return render(request,"vendor/category_decor.html",context=context, status=200)
    elif(category == 'photographer'):
        return render(request,"vendor/category_photographer.html",context=context, status=200)
    else:
        return render(request,"vendor/category_view.html",context=context, status=200)
    return render(request,"vendor/category_view.html",context=context, status=200)

@authenticated_vendor
def vendor_detail(request,vendor_name, *args, **kwargs):
    data = {}
    my_vendor = None
    checkimage = FilesAndImages()
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
        data = checkimage.getPhotgrapherPackage(my_vendor.type, my_vendor, data)
    return render(request,"vendor/vendor_details.html",context=data, status=200)


def schedule_meeting_list(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    data = {}
    checkimage = FilesAndImages()
    try:
        username = User.objects.get(username=request.user)
        all_my_vendors = username.uppervendor_set.all()
        confirm_schedule_list =[]; pending_schedule_list =[]
        for vendor in all_my_vendors:
            schedule = ScheduleMeeting.objects.filter(service=vendor)
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

def pending_schedule(request, *args, **kwargs):
    if request.method == 'POST':
        form = EditScheduleForm(request.POST)
        if form.is_valid():
            if (request.POST.get("confirm")):
                d1 = form.confirmSchedule()
            elif(request.POST.get("cancel")):
                d1 = form.deletingSchedule()
            return redirect(f"/Vendor/u/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/")

def canceling_schedule(request, *args, **kwargs):
    if request.method == 'POST':
        form = EditScheduleForm(request.POST)
        if form.is_valid():
            d1 = form.deletingSchedule()
            return redirect(f"/Vendor/u/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/")

def testing(request):
    data={}
    return render(request, "testing.html",context=data, status=200)

def getFoodDetails(request, package_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    data = {}
    try:
        package_detail = VendorFood.objects.get(id=int(package_id))
        vendor_list = {}
        vendor_list = {
                'package_name':package_detail.package_name,
                'salads':package_detail.salads,
                'veg_starter': package_detail.veg_starter,
                'veg_main_course': package_detail.veg_main_course,
                'raita':package_detail.raita,
                'dessert': package_detail.dessert,
                'rotis_bread': package_detail.rotis_bread,
                'rice_biryani':package_detail.rice_biryani,
                'dal': package_detail.dal,
                'welcome_drinks': package_detail.welcome_drinks,
                'soup': package_detail.soup,
                'non_veg_food':package_detail.non_veg_food
            }
        if(package_detail.non_veg_food==True):
            vendor_list['non_veg_starter'] = package_detail.non_veg_starter
            vendor_list['non_veg_main_course'] = package_detail.non_veg_main_course
            

        data = {
            'vendor_list': vendor_list
        }
            
    except Exception as e:
        print("Vendor: ", str(e))
    return JsonResponse(data)

def getDecorDetails(request, package_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    data = {}
    try:
        package_detail = VendorDecor.objects.get(id=int(package_id))
        vendor_list = {}
        vendor_list = {
                'package_name':package_detail.package_name,
                'stage':'Yes' if (package_detail.stage) else 'No',
                'lights': 'Yes' if (package_detail.lights) else 'No',
                'flowers': 'Yes' if (package_detail.flowers) else 'No',
                'furniture':'Yes' if (package_detail.furniture) else 'No',
                'entrance': 'Yes' if (package_detail.entrance) else 'No',
                'lounge': 'Yes' if (package_detail.lounge) else 'No'
            }
        data = {
            'vendor_list': vendor_list
        }
            
    except Exception as e:
        print("Vendor: ", str(e))
    return JsonResponse(data)

def getPhotographerDetails(request, package_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    data = {}
    try:
        package_detail = VendorPhotographer.objects.get(id=int(package_id))
        vendor_list = {
            'package_name':package_detail.package_name
        }
        if(package_detail.candid_photo):
            vendor_list['candid_photo'] = "Yes"
            vendor_list['candid_photo_dur'] = package_detail.candid_photo_dur
            vendor_list['candid_person'] = package_detail.candid_person
        else:
            vendor_list['candid_photo'] = "No"
            vendor_list['candid_photo_dur'] = "NA"
            vendor_list['candid_person'] = "NA"
        
        if(package_detail.event_photo):
            vendor_list['event_photo'] = "Yes"
            vendor_list['event_photo_dur'] = package_detail.event_photo_dur
            vendor_list['event_person'] = package_detail.event_person
        else:
            vendor_list['candid_photo'] = "No"
            vendor_list['candid_photo_dur'] = "NA"
            vendor_list['event_person'] = "NA"
        
        if(package_detail.videography):
            vendor_list['videography'] = "Yes"
            vendor_list['video_dur'] = package_detail.video_dur
            vendor_list['video_person'] = package_detail.video_person
        else:
            vendor_list['videography'] = "No"
            vendor_list['video_dur'] = "NA"
            vendor_list['video_person'] = "NA"
        data = {
            'vendor_list': vendor_list
        }
            
    except Exception as e:
        print("Vendor: ", str(e))
    return JsonResponse(data)


def deleteService(request, *args, **kwargs):
    if request.method == 'POST':
        form = DeleteService(request.POST)
        if form.is_valid():
            d1 = form.deleteOtherReference()
            return redirect(f"/Vendor/u/")
        else:
            print("Error 1")
            raise Http404
    else:
        redirect("/Vendor/")