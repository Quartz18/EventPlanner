from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, Http404
from VendorApp.models import UpperVendor, Venue, Caterer, Decor, Photographer
from VendorApp.files import FilesAndImages
from .models import City
from .forms import UserSignUpForm, VendorSignUpForm
from .decorators import unauthenticated_user, authenticated_vendor, authenticated_user, authenticate_all_user
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


# Create your views here.
def convertIntoJSON(my_vendor):
    vendor_list = []
    checkimage = FilesAndImages()
    for vendor in my_vendor:
        data1 = {
            'id': vendor.pk,
            'name': str(vendor.vendor_name),
            'type': vendor.type,
            'address': vendor.vendor_address,
        }
        data1 = checkimage.uploadImage(vendor, data1)
        vendor_list.append(data1)
    return vendor_list

@unauthenticated_user
def home_view(request, *args, **kwargs):
    return render(request,"home_view.html",context={}, status=200)

@unauthenticated_user
def register_view(request, *args, **kwargs):
    return render(request,"register_login.html",context={}, status=200)

@unauthenticated_user
def vendor_register_view(request, *args, **kwargs):
    return render(request,"vendor_register.html",context={}, status=200)

@unauthenticated_user
def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request,user_)
        if(user_.type == 'VENDOR'):
            return redirect("/Vendor/")
        else:
            return redirect("/u/")
    return redirect("/Register/")

def register_user(request, *args, **kwargs):
    username = request.POST.get("username") or None
    email = request.POST.get("email") or None
    password = request.POST.get("password") or None
    confirm_password = request.POST.get("confirm_password")
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            username,email,password = form.clean_content()
            #print(username)
            obj2 = form.saveUser()
            #print(obj2)
            login(request,obj2)
            return redirect("/")
        else:
            raise Http404
    return redirect("/Register/")

def register_vendor(request, *args, **kwargs):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            username,email,password = form.clean_content()
            obj2 = form.saveVendor()
            login(request,obj2)
            return redirect("/Vendor/")
        else:
            raise Http404
            
    # form = UserCreationForm()
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    return redirect("/Register/")

@authenticate_all_user
def logout_view(request, *args, **kwargs):
    # if request.method == "POST":
    #     logout(request)
    #     return redirect("/")
    logout(request)
    return redirect("/")

def city_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    city = City.objects.all()
    city_list =[{'id':x.pk,'name':x.city_name} for x in city]
    data = {
        'response' : city_list
    }
    return JsonResponse(data)

def general_list_view(request,category,*args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    my_vendor = None
    if(category == 'venue'):
        my_vendor = Venue.objects.all()
    elif(category == 'caterer'):
        my_vendor = Caterer.objects.all()
    elif(category == 'decor'):
        my_vendor = Decor.objects.all()
    elif(category == 'photographer'):
        my_vendor = Photographer.objects.all()
    else:
        my_vendor = UpperVendor.objects.all()
    vendor_list = convertIntoJSON(my_vendor)
    data = {
        'response': vendor_list
    }
    return JsonResponse(data)

def vendor_list_view(request, city_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    city = City.objects.get(id = city_id)
    my_vendor = city.uppervendor_set.all()
    vendor_list = []
    checkimage = FilesAndImages()
    for vendor in my_vendor:
        data1 = {
            'id': vendor.pk,
            'name': str(vendor.vendor_name),
            'type': vendor.type,
            'address': vendor.vendor_address,
        }
        data1 = checkimage.uploadImage(vendor, data1)
        vendor_list.append(data1)
    data = {
        'response': vendor_list,
    }
    return JsonResponse(data)

@unauthenticated_user
def category_view(request,category, *args, **kwargs):
    if(category == 'venue'):
        return render(request,"category_venue.html",context={}, status=200)
    elif(category == 'caterer'):
        return render(request,"category_caterer.html",context={}, status=200)
    elif(category == 'decor'):
        return render(request,"category_decor.html",context={}, status=200)
    elif(category == 'photographer'):
        return render(request,"category_photographer.html",context={}, status=200)
    else:
        return render(request,"category_view.html",context={}, status=200)
    return render(request,"category_view.html",context={}, status=200)


def category_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    my_venue = Venue.objects.all()
    my_caterer = Caterer.objects.all()
    my_decor = Decor.objects.all()
    my_photographer = Photographer.objects.all()
    #my_venue = city.uppervendor_set.filter(type="VENUE")
    my_vendor = [my_venue, my_caterer, my_decor, my_photographer]
    result = list(map(convertIntoJSON, my_vendor))
    data = {
        'my_venue': result[0],
        'my_caterer': result[1],
        'my_decor': result[2],
        'my_photographer': result[3]
    }
    return JsonResponse(data)

def category_city_view(request,category,city_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    city = City.objects.get(id=city_id)
    my_vendor = None
    if(category=='venue'):
        my_vendor = city.uppervendor_set.filter(type="VENUE")
    elif(category == 'caterer'):
        my_vendor = city.uppervendor_set.filter(type="CATERER")
    elif(category == 'decor'):
        my_vendor = city.uppervendor_set.filter(type="DECOR")
    elif(category == 'photographer'):
        my_vendor = city.uppervendor_set.filter(type="PHOTOGRAPHER")
    vendor_list = convertIntoJSON(my_vendor)
    data = {
        'response': vendor_list
    }
    return JsonResponse(data)

def general_city_view(request,city_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/Android
    return json data
    """
    city = City.objects.get(id=city_id)
    my_venue = city.uppervendor_set.filter(type="VENUE")
    my_caterer = city.uppervendor_set.filter(type="CATERER")
    my_decor = city.uppervendor_set.filter(type="DECOR")
    my_photographer = city.uppervendor_set.filter(type="PHOTOGRAPHER")
    #my_venue = city.uppervendor_set.filter(type="VENUE")
    my_vendor = [my_venue, my_caterer, my_decor, my_photographer]
    result = list(map(convertIntoJSON, my_vendor))
    data = {
        'my_venue': result[0],
        'my_caterer': result[1],
        'my_decor': result[2],
        'my_photographer': result[3]
    }
    return JsonResponse(data)

@unauthenticated_user
def vendor_profile_detail(request,vendor_name, *args, **kwargs):
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
        print("Public Profile:", e)
    else:
        data = checkimage.getFiles(my_vendor, data)
        data = checkimage.getPolicyandTime(my_vendor.type,my_vendor,data)
        data = checkimage.uploadImage(my_vendor, data)
        data = checkimage.getPartArea(my_vendor.type, my_vendor, data)
        data = checkimage.getFoodPackage(my_vendor.type, my_vendor, data)
        data = checkimage.getDecorPackage(my_vendor.type, my_vendor, data)
        data = checkimage.getPhotgrapherPackage(my_vendor.type, my_vendor, data)
    return render(request,"details.html",context=data, status=200)
