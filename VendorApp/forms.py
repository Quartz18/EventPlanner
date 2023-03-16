from django import forms
from .models import UpperVendor, VendorTiming, VenuePolicy, VendorPolicy, PartArea, VendorFood, VendorDecor, VendorPhotographer
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from Account.models import User
from ClientApp.models import ScheduleMeeting
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta

class VendorForm(forms.ModelForm):
    class Meta:
        model = UpperVendor
        fields = [
            'type',
            'vendor_name',
            'vendor_address',
            'vendor_about',
            'vendor_contact_name',
            'vendor_contact_number',
            'city',
            ]
        widgets = {
            'type' : forms.Select(attrs={'id':'type', 'required':'True'}),
            'vendor_name' : forms.TextInput(attrs={'id': 'vendor_name', 'placeholder':' Registered Name', 'required':'True'}),
            'vendor_address' : forms.Textarea(attrs={'id': 'vendor_address', 'placeholder':'Address', 'rows': 3, 'required':'True'}),
            'vendor_about' : forms.FileInput(attrs={'id': 'vendor_about', 'placeholder':'Summary', 'required':'True'}),
            'vendor_contact_name' : forms.TextInput(attrs={'id': 'vendor_contact_name', 'placeholder':' Contact Name','required':'True'}),
            'city': forms.Select(attrs={'id':'city', 'required':'True'}),
            'vendor_contact_number' : forms.TextInput(attrs={'id': 'vendor_contact_number', 'title':'', 'placeholder':'Contact Number','required':'True'})
        }
        labels = {
            'type': _(''),
            'vendor_name':_(''),
            'vendor_address':_(''),
            'vendor_about':_(''),
            'vendor_contact_name':_(''),
            'vendor_contact_number':_(''),
            'city':_('')
        }

class EditTimeForm(forms.Form):
    opening_time = forms.TimeField(required=True)
    closing_time = forms.TimeField(required=True)
    vendor_name = forms.CharField(max_length=30, required=True)

    def checkTime(self):
        opening_time = self.cleaned_data['opening_time']
        closing_time = self.cleaned_data['closing_time']
        d1 = timedelta(hours=opening_time.hour, minutes=opening_time.minute, seconds=opening_time.second)
        d2 = timedelta(hours=closing_time.hour, minutes=closing_time.minute, seconds=closing_time.second)
        if(d1>d2):
            raise forms.ValidationError("Enter Valid Opening and Closing Time.")
        else:
            return "Proper"
    
    def saveTime(self):
        opening_time = self.cleaned_data['opening_time']
        closing_time = self.cleaned_data['closing_time']
        vendor_name = self.cleaned_data['vendor_name']
        try:
            vendor_name_1 = UpperVendor.objects.get(vendor_name=vendor_name)
            v = VendorTiming.objects.get(vendor_name=vendor_name_1)
            v.vendor_opening_time = opening_time
            v.vendor_closing_time = closing_time
            v.save()
        except Exception as e:
            return str(e)
        return "Saved"

class EditImageForm(forms.Form):
    vendor_name = forms.CharField(max_length=30, required=True)
    vendor_image = forms.ImageField(required=True)
    category = forms.CharField(max_length=20, required=True)
    def checkImage(self):
        vendor_image = self.cleaned_data['vendor_image']
        vendor_name = self.cleaned_data['vendor_name']
        category = self.cleaned_data['category']
        vendor_name_1 =None
        category_list = ["VENUE", "CATERER", "DECOR", "PHOTOGRAPHER"]
        if category not in category_list:
            raise forms.ValidationError(category," is not a valid category.")
        try:
            vendor_name_1 = UpperVendor.objects.get(vendor_name=vendor_name)
        except Exception as e:
            return str(e)
        if vendor_name_1 == None:
            raise forms.ValidationError(category," is not a valid vendor name.")

        return vendor_name_1, category
        
class EditAddressForm(forms.Form):
    vendor_address =forms.CharField(max_length=255,required=True,widget=forms.Textarea)
    vendor_name = forms.CharField(max_length=30, required=True)
    def updateAddress(self):
        vendor_address = self.cleaned_data['vendor_address']
        vendor_name = self.cleaned_data['vendor_name']
        try:
            if len(vendor_address)<30:
                raise forms.ValidationError("Provide a valid address.")
            else:
                up = UpperVendor.objects.get(vendor_name=vendor_name)
                up.vendor_address = vendor_address
                up.save()
        except Exception as e:
            print(e)
        return "Saved"

class EditContactForm(forms.Form):
    vendor_contact_name =forms.CharField(max_length=25,required=True)
    vendor_contact_number = forms.CharField(max_length=12)
    vendor_name = forms.CharField(max_length=30, required=True)
    def updateContact(self):
        vendor_contact_name = self.cleaned_data['vendor_contact_name']
        vendor_contact_number = self.cleaned_data['vendor_contact_number']
        vendor_name = self.cleaned_data['vendor_name']
        try:
            up = UpperVendor.objects.get(vendor_name=vendor_name)
            up.vendor_contact_name = vendor_contact_name
            up.vendor_contact_number = vendor_contact_number
            up.save()
        except Exception as e:
            print(e)
        return "Saved"

class EditPolicyForm(forms.Form):
    vendor_name = forms.CharField(required=True)
    category = forms.CharField(required=True)
    venue_decor = forms.IntegerField(required=False)
    outside_decor = forms.BooleanField(required=False)
    venue_halls_ac = forms.BooleanField(required=False)
    venue_room_available = forms.BooleanField(required=False)
    venue_room_count = forms.IntegerField(required=False)
    venue_room_ac = forms.IntegerField(required=False)
    room_avg_price = forms.IntegerField(required=False)
    room_ac_avg_price = forms.IntegerField(required=False)
    changing_room_count = forms.IntegerField(required=False)
    changing_room_count_ac = forms.IntegerField(required=False)
    advance_percentage = forms.IntegerField(required=False)
    cancellation = forms.BooleanField(required=False)
    parking_valet = forms.BooleanField(required=False)
    parking_space_count = forms.IntegerField(required=False)
    alcohol_allowance = forms.BooleanField(required=False)
    outside_alcohol = forms.BooleanField(required=False)
    music_allowance = forms.BooleanField(required=False)
    late_music_allowance = forms.BooleanField(required=False)
    firecrackers = forms.BooleanField(required=False)
    overnight_function = forms.BooleanField(required=False)
    vendor_yrs_exp = forms.IntegerField(required=False)
    events_completed = forms.IntegerField(required=False)
    vendor_usp = forms.CharField(max_length=255,required=False,widget=forms.Textarea)
    travel_allowance = forms.BooleanField(required=False)
    outside_travel_price = forms.BooleanField(required=False)
    def updatePolicy(self):
        venue_decor = self.cleaned_data['venue_decor']
        category = self.cleaned_data['category']
        policy_name = self.cleaned_data['vendor_name']
        outside_decor = self.cleaned_data['outside_decor']
        venue_halls_ac = self.cleaned_data['venue_halls_ac']
        venue_room_available = self.cleaned_data['venue_room_available']
        venue_room_count = self.cleaned_data['venue_room_count']
        venue_room_ac = self.cleaned_data['venue_room_ac']
        room_avg_price = self.cleaned_data['room_avg_price']
        room_ac_avg_price = self.cleaned_data['room_ac_avg_price']
        changing_room_count = self.cleaned_data['changing_room_count']
        changing_room_count_ac = self.cleaned_data['changing_room_count_ac']
        advance_percentage = self.cleaned_data['advance_percentage']
        cancellation = self.cleaned_data['cancellation']
        parking_valet = self.cleaned_data['parking_valet']
        parking_space_count = self.cleaned_data['parking_space_count']
        alcohol_allowance = self.cleaned_data['alcohol_allowance']
        outside_alcohol = self.cleaned_data['outside_alcohol']
        music_allowance = self.cleaned_data['music_allowance']
        late_music_allowance = self.cleaned_data['late_music_allowance']
        firecrackers = self.cleaned_data['firecrackers']
        overnight_function = self.cleaned_data['overnight_function']
        vendor_yrs_exp = self.cleaned_data['vendor_yrs_exp']
        events_completed = self.cleaned_data['events_completed']
        vendor_usp = self.cleaned_data['vendor_usp']
        travel_allowance = self.cleaned_data['travel_allowance']
        outside_travel_price = self.cleaned_data['outside_travel_price']
        category_list = ["VENUE", "CATERER", "DECOR", "PHOTOGRAPHER"]
        if category not in category_list:
            raise forms.ValidationError(category," is not a valid category.")
        elif category == "VENUE":
            try:
                up = UpperVendor.objects.get(vendor_name=policy_name)
                venue_policy = VenuePolicy.objects.get(policy_name=up)
                if venue_decor !=None and venue_decor>=0:
                    venue_policy.venue_decor = venue_decor
                if outside_decor == True:
                    venue_policy.outside_decor = True
                else:
                    venue_policy.outside_decor = False
                if venue_halls_ac == True:
                    venue_policy.venue_halls_ac = True
                else:
                    venue_policy.venue_halls_ac = False
                if cancellation == True:
                    venue_policy.cancellation = True
                else:
                    venue_policy.cancellation = False
                if venue_room_available == True:
                    venue_policy.venue_room_available = True
                else:
                    venue_policy.venue_room_available = False
                if venue_room_count != None and venue_room_count >=0:
                    venue_policy.venue_room_count = venue_room_count
                if venue_room_ac != None and venue_room_ac >=0:
                    venue_policy.venue_room_ac = venue_room_ac
                if room_avg_price !=None and room_avg_price >=0:
                    venue_policy.room_avg_price = room_avg_price
                if room_ac_avg_price != None and room_ac_avg_price >=0:
                    venue_policy.room_ac_avg_price = room_ac_avg_price
                if changing_room_count != None and changing_room_count >=0:
                    venue_policy.changing_room_count = changing_room_count
                if changing_room_count_ac != None and changing_room_count_ac >=0:
                    venue_policy.changing_room_count_ac = changing_room_count_ac
                if advance_percentage != None and advance_percentage>=0 and advance_percentage <=0:
                    venue_policy.advance_percentage = advance_percentage
                if parking_valet == True:
                    venue_policy.parking_valet = True
                else:
                    venue_policy.parking_valet = False
                if parking_space_count != None and parking_space_count>=0:
                    venue_policy.parking_space_count = parking_space_count
                if alcohol_allowance == True:
                    venue_policy.alcohol_allowance = True
                else:
                    venue_policy.alcohol_allowance = False
                if outside_alcohol == True:
                    venue_policy.outside_alcohol = True
                else:
                    venue_policy.outside_alcohol = False
                if music_allowance == True:
                    venue_policy.music_allowance = True
                else:
                    venue_policy.music_allowance = False
                if late_music_allowance == True:
                    venue_policy.late_music_allowance = True
                else:
                    venue_policy.late_music_allowance = False
                if firecrackers == True:
                    venue_policy.firecrackers = True
                else:
                    venue_policy.firecrackers = False
                if overnight_function == True:
                    venue_policy.overnight_function = True
                else:
                    venue_policy.overnight_function = False
                venue_policy.save()
            except Exception as e:
                print(e)
        else:
            try:
                up = UpperVendor.objects.get(vendor_name=policy_name)
                venue_policy = VendorPolicy.objects.get(vendor_name=up, category=category)
                if vendor_yrs_exp != None and vendor_yrs_exp >=0:
                    venue_policy.vendor_yrs_exp = vendor_yrs_exp
                if events_completed != None and events_completed >=0:
                    venue_policy.events_completed = events_completed
                if travel_allowance == True:
                    venue_policy.travel_allowance = True
                else:
                    venue_policy.travel_allowance = False
                if outside_travel_price != None and outside_travel_price >=0:
                    venue_policy.outside_travel_price = outside_travel_price
                if cancellation == True:
                    venue_policy.cancellation = True
                else:
                    venue_policy.cancellation = False
                if advance_percentage != None and advance_percentage>=0 and advance_percentage <=0:
                    venue_policy.advance_percentage = advance_percentage
                if vendor_usp != None:
                    venue_policy.vendor_usp = vendor_usp
                venue_policy.save()
            except Exception as e:
                print(e)
        return "Saved"


class EditPartyForm(forms.Form):
    vendor_name = forms.CharField(max_length=30, required=True)
    category = forms.CharField(max_length=20, required=True)
    area_name = forms.CharField(max_length=20, required=True)
    seating = forms.IntegerField(required=True)
    max_capacity = forms.IntegerField(required=True)
    price = forms.IntegerField(required=True)
    def addPartyArea(self):
        vendor_name = self.cleaned_data['vendor_name']
        category = self.cleaned_data['category']
        area_name = self.cleaned_data['area_name']
        seating = self.cleaned_data['seating']
        max_capacity = self.cleaned_data['max_capacity']
        price = self.cleaned_data['price']
        vendor_name_1 =None
        category_list = ["VENUE", "CATERER", "DECOR", "PHOTOGRAPHER"]
        form_fields = [vendor_name, category, area_name, seating, max_capacity, price]
        if None in form_fields:
            raise forms.ValidationError("Field cannot be empty.")
        elif category not in category_list:
            raise forms.ValidationError(category," is not a valid category.")
        elif seating < 0 or max_capacity<0 or price<0:
            raise forms.ValidationError("Value cannot be in negative number.")
        try:
            vendor_name_1 = UpperVendor.objects.get(vendor_name=vendor_name)
        except Exception as e:
            return str(e)
        else:
            party_area = PartArea(venue_name=vendor_name_1, category=category, area_name=area_name, seating=seating, max_capacity=max_capacity, price=price)
            party_area.save()
        if vendor_name_1 == None:
            raise forms.ValidationError(category," is not a valid vendor name.")

        return vendor_name_1, category


class EditFoodForm(forms.Form):
    vendor_name = forms.CharField(max_length=30, required=True)
    category = forms.CharField(max_length=20, required=True)
    package_name = forms.CharField(max_length=20, required=True)
    package_price = forms.IntegerField(required=True)
    max_capacity = forms.IntegerField(required=True)
    salads = forms.IntegerField(required=False)
    veg_starter = forms.IntegerField(required=False)
    veg_main_course = forms.IntegerField(required=False)
    raita = forms.IntegerField(required=False)
    dessert = forms.IntegerField(required=False)
    rotis_bread = forms.IntegerField(required=False)
    rice_biryani = forms.IntegerField(required=False)
    dal = forms.IntegerField(required=False)
    welcome_drinks = forms.IntegerField(required=False)
    soup = forms.IntegerField(required=False)
    non_veg_food = forms.BooleanField(required=False)
    non_veg_starter = forms.IntegerField(required=False)
    non_veg_main_course = forms.IntegerField(required=False)
    def CheckForEmpty(self,form_fields):
        for x in range(0, len(form_fields)):
            if form_fields[x] == None: 
                form_fields[x] = 0
        return form_fields
    def CheckForLess(self,form_fields1, form_fields2):
        for x in form_fields2:
            if x < 0: 
                return True
        for x in form_fields1[3::]:
            if x < 0: 
                return True
        return False
    def addFood(self):
        vendor_name = self.cleaned_data['vendor_name']
        category = self.cleaned_data['category']
        package_name = self.cleaned_data['package_name']
        package_price = self.cleaned_data['package_price']
        max_capacity = self.cleaned_data['max_capacity']
        salads = self.cleaned_data['salads']
        veg_starter = self.cleaned_data['veg_starter']
        veg_main_course = self.cleaned_data['veg_main_course']
        raita = self.cleaned_data['raita']
        dessert = self.cleaned_data['dessert']
        rotis_bread = self.cleaned_data['rotis_bread']
        rice_biryani = self.cleaned_data['rice_biryani']
        dal = self.cleaned_data['dal']
        welcome_drinks = self.cleaned_data['welcome_drinks']
        soup = self.cleaned_data['soup']
        non_veg_food = self.cleaned_data['non_veg_food']
        non_veg_starter = self.cleaned_data['non_veg_starter']
        non_veg_main_course = self.cleaned_data['non_veg_main_course']
        vendor_name_1 =None
        category_list = ["VENUE", "CATERER", "DECOR", "PHOTOGRAPHER"]
        form_fields = [[vendor_name, category, package_name, package_price, max_capacity],[ salads,veg_starter,veg_main_course, raita, dessert, rotis_bread, rice_biryani, dal, welcome_drinks, soup,non_veg_starter, non_veg_main_course]]
        form_fields1 = self.CheckForEmpty(form_fields[1])
        if None in form_fields[0]:
            raise forms.ValidationError("Field cannot be empty.")
        elif category not in category_list:
            raise forms.ValidationError(category," is not a valid category.")
        elif self.CheckForLess(form_fields[0],form_fields1):
            raise forms.ValidationError("Value cannot be in negative number.")
        try:
            vendor_name_1 = UpperVendor.objects.get(vendor_name=vendor_name)
        except Exception as e:
            return str(e)
        else:
            vendor_food = VendorFood(
                vendor_name=vendor_name_1,
                category=category,
                package_name=package_name,
                package_price=package_price,
                max_capacity=max_capacity,
                salads=form_fields1[0],
                veg_starter=form_fields1[1],
                veg_main_course=form_fields1[2],
                raita=form_fields1[3],
                dessert=form_fields1[4],
                rotis_bread=form_fields1[5],
                rice_biryani=form_fields1[6],
                dal=form_fields1[7],
                welcome_drinks=form_fields1[8],
                soup=form_fields1[9],
                non_veg_food=non_veg_food,
                non_veg_starter=form_fields1[10],
                non_veg_main_course=form_fields1[11]
            )
            vendor_food.save()
        if vendor_name_1 == None:
            raise forms.ValidationError(category," is not a valid vendor name.")

        return vendor_name_1, category

class EditDecorForm(forms.Form):
    vendor_name = forms.CharField(max_length=30, required=True)
    category = forms.CharField(max_length=20, required=True)
    package_name = forms.CharField(max_length=20, required=True)
    package_price = forms.IntegerField(required=True)
    max_capacity = forms.IntegerField(required=True)
    stage = forms.BooleanField(required=False)
    lights = forms.BooleanField(required=False)
    flowers = forms.BooleanField(required=False)
    furniture = forms.BooleanField(required=False)
    entrance = forms.BooleanField(required=False)
    lounge = forms.BooleanField(required=False)
    def CheckForEmpty(self,form_fields):
        for x in range(0, len(form_fields)):
            if form_fields[x] == None: 
                form_fields[x] = 0
        return form_fields
    def CheckForLess(self,form_fields1):
        for x in form_fields1[3::]:
            if x < 0: 
                return True
        return False
    def addDecor(self):
        vendor_name = self.cleaned_data['vendor_name']
        category = self.cleaned_data['category']
        package_name = self.cleaned_data['package_name']
        package_price = self.cleaned_data['package_price']
        max_capacity = self.cleaned_data['max_capacity']
        stage = self.cleaned_data['stage']
        lights = self.cleaned_data['lights']
        flowers = self.cleaned_data['flowers']
        furniture = self.cleaned_data['furniture']
        entrance = self.cleaned_data['entrance']
        lounge = self.cleaned_data['lounge']
        vendor_name_1 =None
        category_list = ["VENUE", "CATERER", "DECOR", "PHOTOGRAPHER"]
        form_fields = [[vendor_name, category, package_name, package_price, max_capacity],[ stage,lights,flowers, furniture, entrance, lounge]]
        form_fields1 = self.CheckForEmpty(form_fields[1])
        if None in form_fields[0]:
            raise forms.ValidationError("Field cannot be empty.")
        elif category not in category_list:
            raise forms.ValidationError(category," is not a valid category.")
        elif self.CheckForLess(form_fields[0]):
            raise forms.ValidationError("Value cannot be in negative number.")
        try:
            vendor_name_1 = UpperVendor.objects.get(vendor_name=vendor_name)
        except Exception as e:
            return str(e)
        else:
            vendor_food = VendorDecor(
                vendor_name=vendor_name_1,
                category=category,
                package_name=package_name,
                package_price=package_price,
                max_capacity=max_capacity,
                stage=form_fields1[0],
                lights=form_fields1[1],
                flowers=form_fields1[2],
                furniture=form_fields1[3],
                entrance=form_fields1[4],
                lounge=form_fields1[5]
            )
            vendor_food.save()
        if vendor_name_1 == None:
            raise forms.ValidationError(category," is not a valid vendor name.")

        return vendor_name_1, category

class EditPhotographerForm(forms.Form):
    vendor_name = forms.CharField(max_length=30, required=True)
    category = forms.CharField(max_length=20, required=True)
    package_name = forms.CharField(max_length=20, required=True)
    package_price = forms.IntegerField(required=True)
    candid_photo = forms.BooleanField(required=False)
    candid_photo_dur = forms.IntegerField(required=False)
    candid_person = forms.IntegerField(required=False)
    event_photo = forms.BooleanField(required=False)
    event_photo_dur = forms.IntegerField(required=False)
    event_person = forms.IntegerField(required=False)
    videography = forms.BooleanField(required=False)
    video_dur = forms.IntegerField(required=False)
    video_person = forms.IntegerField(required=False)
    main_dur = forms.IntegerField(required=True)
    def CheckForEmpty(self,form_fields):
        for x in range(0, len(form_fields)):
            if form_fields[x] == None: 
                form_fields[x] = 0
        return form_fields
    def CheckForLess(self,form_fields1):
        for x in form_fields1[3::]:
            if x < 0: 
                return True
        return False
    def CheckForMore(self,form_fields1):
        for x in range(1, len(form_fields1),2):
            if form_fields1[x]>7: 
                return True
        return False
    def addPhotograher(self):
        vendor_name = self.cleaned_data['vendor_name']
        category = self.cleaned_data['category']
        package_name = self.cleaned_data['package_name']
        package_price = self.cleaned_data['package_price']
        candid_photo = self.cleaned_data['candid_photo']
        candid_photo_dur = self.cleaned_data['candid_photo_dur']
        candid_person = self.cleaned_data['candid_person']
        event_photo = self.cleaned_data['event_photo']
        event_photo_dur = self.cleaned_data['event_photo_dur']
        event_person = self.cleaned_data['event_person']
        videography = self.cleaned_data['videography']
        video_dur = self.cleaned_data['video_dur']
        video_person = self.cleaned_data['video_person']
        main_dur = self.cleaned_data['main_dur']
        vendor_name_1 =None
        category_list = ["VENUE", "CATERER", "DECOR", "PHOTOGRAPHER"]
        form_fields = [[vendor_name, category, package_name, package_price, main_dur],[ candid_photo,candid_photo_dur,candid_person, event_photo,event_photo_dur, event_person, videography,video_dur, video_person]]
        form_fields1 = self.CheckForEmpty(form_fields[1])
        if None in form_fields[0]:
            raise forms.ValidationError("Field cannot be empty.")
        elif category not in category_list:
            raise forms.ValidationError(category," is not a valid category.")
        elif self.CheckForLess(form_fields[0]):
            raise forms.ValidationError("Value cannot be in negative number.")
        elif self.CheckForMore(form_fields[1]) or main_dur>7:
            raise forms.ValidationError("Value cannot be grater than 7.")
        try:
            vendor_name_1 = UpperVendor.objects.get(vendor_name=vendor_name)
        except Exception as e:
            return str(e)
        else:
            vendor_food = VendorPhotographer(
                vendor_name=vendor_name_1,
                category=category,
                package_name=package_name,
                package_price=package_price,
                candid_photo=form_fields1[0],
                candid_photo_dur=form_fields1[1],
                candid_person=form_fields1[2],
                event_photo=form_fields1[3],
                event_photo_dur=form_fields1[4],
                event_person=form_fields1[5],
                videography=form_fields1[6],
                video_dur=form_fields1[7],
                video_person=form_fields1[8],
                main_dur=form_fields[0][4]
            )
            vendor_food.save()
        if vendor_name_1 == None:
            raise forms.ValidationError(category," is not a valid vendor name.")

        return vendor_name_1, category

class EditNameForm(forms.Form):
    vendor_name = forms.CharField(max_length=50, required=True)
    service_name = forms.CharField(max_length=50, required=True)
    def updateName(self):
        vendor_name = self.cleaned_data['vendor_name']
        service_name = self.cleaned_data['service_name']
        vendor_name_1 =None
        if None in [vendor_name, service_name]:
            raise forms.ValidationError("Field cannot be empty.")
        try:
            vendor_name_1 = UpperVendor.objects.get(vendor_name=vendor_name)
        except Exception as e:
            return str(e)
        else:
            vendor_name_1.vendor_name = service_name
            vendor_name_1.save()
        if vendor_name_1 == None:
            raise forms.ValidationError(vendor_name," is not a valid vendor name.")

        return vendor_name_1


class EditScheduleForm(forms.Form):
    service = forms.CharField(max_length=50, required=True)
    client = forms.CharField(max_length=50, required=True)
    def confirmSchedule(self):
        service = self.cleaned_data['service']
        client = self.cleaned_data['client']
        try:
            user_client = User.objects.get(username=client)
            up = UpperVendor.objects.get(vendor_name=service)
            scheduling = ScheduleMeeting.objects.get(service=up, client=user_client)
            scheduling.confirm_schedule = True
            scheduling.save()
        except Exception as e:
            print("Confirm of meeting was not successfully: ",e)
        return "saved"
    
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

class DeleteService(forms.Form):
    vendor_name = forms.CharField(max_length=50, required=True)
    def deleteOtherReference(self):
        vendor_name = self.cleaned_data['vendor_name']
        try:
            up = UpperVendor.objects.get(vendor_name=vendor_name)
            if (up.type == 'VENUE'):
                up.vendorimage_set.all().delete()
                up.vendortiming.delete()
                up.vendordecor_set.all().delete()
                up.vendorfood_set.all().delete()
                up.partarea_set.all().delete()
                up.venuepolicy.delete()
                up.delete()
            elif (up.type == 'CATERER'):
                up.vendorimage_set.all().delete()
                up.vendortiming.delete()
                up.vendorpolicy.delete()
                up.vendorfood_set.all().delete()
                up.delete()
            elif(up.type == 'DECOR'):
                up.vendorimage_set.all().delete()
                up.vendortiming.delete()
                up.vendorpolicy.delete()
                up.vendordecor_set.all().delete()
                up.delete()
            else:
                up.vendorimage_set.all().delete()
                up.vendortiming.delete()
                up.vendorpolicy.delete()
                up.vendorphotographer_set.all().delete()
                up.delete()
        except Exception as e:
            print(e)
        return "deleted"