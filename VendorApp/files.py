import os
from django.conf import settings
from django.http import HttpRequest, JsonResponse, Http404
from .models import UpperVendor, VendorTiming, VendorPolicy, VenuePolicy, PartArea


class FilesAndImages():

    def __init__(self):
        count = 0
    
    def saveOtherClass(self, type_p, up):
        type_list = ["VENUE", "CATERER", "DECOR", "PHOTOGRAPHER"]
        try:
            print("ok 1")
            print("ok 1.1")
            if type_p not in type_list:
                raise forms.ValidationError(category," is not a valid category.")
            else:
                print("ok 2")
                vi = VendorTiming.objects.create(vendor_name=up,category=type_p)
                if type_p == 'VENUE':
                    vp = VenuePolicy.objects.create(policy_name=up)
                else:
                    print("ok 3")
                    vp = VendorPolicy.objects.create(vendor_name=up,category=type_p)
                    print("ok 4")
            return up.vendor_name
        except Exception as e:
            print("Error: ", str(e))

    def uploadImage(self, my_vendor, data):
        try:
            vendorimage = my_vendor.vendorimage_set.all()
            if vendorimage.exists():
                data['vendorimage'] = str(vendorimage[0].vendor_image.url)
        except Exception as e1:
            print(e1)
        return data

    def getFiles(self, my_vendor, data):
        filename = my_vendor.vendor_about.name
        try:
            file1 = open(os.path.join(settings.MEDIA_ROOT,filename))
            file_list = file1.readlines()
            if(len(file_list)>0):
                if (len(file_list) == 1):
                    data['vendorfile1'] = file_list[0]
                else:
                    
                    data['vendorfile1'] = file_list[0]
                    file2 = file_list[1:]
                    j = ""
                    for i in file2:
                        j+=i
                    data['vendorfile2'] = j
        except Exception as e:
            print(e)
        return data

    def getPolicyandTime(self, category, my_vendor, data):
        try:
            if category == 'VENUE':
                data['vendorpolicy'] = my_vendor.venuepolicy
                data['vendortime'] = my_vendor.vendortiming
                return data
            else:
                data['vendorpolicy'] = my_vendor.vendorpolicy
                data['vendortime'] = my_vendor.vendortiming
                return data
        except Exception as e1:
            print(e1)
        return data
    
    def getPartArea(self, category, my_vendor, data):
        try:
            if category == 'VENUE':
                data['venue_part_area'] = my_vendor.partarea_set.all()
        except Exception as e:
            print(e)
        return data
    
    def getFoodPackage(self, category, my_vendor, data):
        try:
            if category == 'VENUE' or category=='CATERER':
                data['venue_food_package'] = my_vendor.vendorfood_set.all()
        except Exception as e:
            print(e)
        return data
    
    def getDecorPackage(self, category, my_vendor, data):
        try:
            if category == 'VENUE' or category=='DECOR':
                data['venue_decor_package'] = my_vendor.vendordecor_set.all()
        except Exception as e:
            print(e)
        return data
    
    def getPhotgrapherPackage(self, category, my_vendor, data):
        try:
            if category == 'PHOTOGRAPHER':
                data['venue_photographer_package'] = my_vendor.vendorphotographer_set.all()
        except Exception as e:
            print(e)
        return data
 
