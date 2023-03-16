from django.db import models
from phone_field import PhoneField
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from Account.models import User, City
from django.utils.translation import gettext_lazy as _
import datetime
# Create your models here.

#---------------------------------------------------------------------------------------------------
class UpperVendor(models.Model):
    class Types(models.TextChoices):
        VENUE = "VENUE"
        CATERER = "CATERER"
        DECOR = "DECOR"
        PHOTOGRAPHER = "PHOTOGRAPHER"
    type = type = models.CharField(_('Type'),max_length=50,choices=Types.choices, default=Types.VENUE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=120, unique=True)
    vendor_about = models.FileField(upload_to="about/%Y/%m/%D")
    vendor_address = models.TextField()
    vendor_contact_name = models.CharField(max_length=100)
    phone_regrex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone No. must be entered in the format +919999999999.")
    vendor_contact_number = models.CharField(validators=[phone_regrex], max_length=12)
    vendor_taxes = models.CharField(max_length=20,default="F&B : 18.00 %")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    c_log = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor_name

class VenueManager(models.Manager):
    def get_queryset(self):
        return super(VenueManager, self).get_queryset().filter(type = UpperVendor.Types.VENUE)

class CatererManager(models.Manager):
    def get_queryset(self):
        return super(CatererManager, self).get_queryset().filter(type = UpperVendor.Types.CATERER)

class DecorManager(models.Manager):
    def get_queryset(self):
        return super(DecorManager, self).get_queryset().filter(type = UpperVendor.Types.DECOR)

class PhotographerManager(models.Manager):
    def get_queryset(self):
        return super(PhotographerManager, self).get_queryset().filter(type = UpperVendor.Types.PHOTOGRAPHER)

class Venue(UpperVendor):
    objects = VenueManager()
    class Meta:
        proxy = True

class Caterer(UpperVendor):
    objects = CatererManager()
    class Meta:
        proxy = True

class Decor(UpperVendor):
    objects = DecorManager()
    class Meta:
        proxy = True

class Photographer(UpperVendor):
    objects = PhotographerManager()
    class Meta:
        proxy = True

#---------------------------------------------------------------------------------------------------

class VendorPolicy(models.Model):
    vendor_name = models.OneToOneField(UpperVendor, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, default='CATERER')
    vendor_yrs_exp = models.IntegerField(default=0)
    events_completed = models.IntegerField(default=0)
    vendor_usp = models.TextField(default='None')
    travel_allowance = models.BooleanField(default=False)
    outside_travel_price = models.BooleanField(default=False)
    max_value = MaxValueValidator(100,message="Value cannot be more than 100%")
    advance_percentage = models.IntegerField(default=25, validators=[max_value])
    cancellation = models.BooleanField(default=False)

    def __str__(self):
        return self.vendor_name.vendor_name

class VendorImage(models.Model):
    vendor_name = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)
    vendor_image = models.ImageField(upload_to="images/")
    category = models.CharField(max_length=20, default='CATERER')
    
    def __str__(self):
        return self.category

class VendorTiming(models.Model):
    vendor_name = models.OneToOneField(UpperVendor, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, default='VENUE')
    vendor_opening_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.time(10,0,0))
    vendor_closing_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.time(23,0,0))
    morning_opening_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.time(10,0,0))
    morning_closing_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.time(16,0,0))
    evening_opening_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.time(17,0,0))
    evening_closing_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.time(23,0,0))

    def __str__(self):
        return self.vendor_name.vendor_name

# #---------------------------------------------------------------------------------------------------

class VendorDecor(models.Model):
    vendor_name = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, default='DECOR')
    package_name = models.CharField(max_length=120)
    package_price = models.IntegerField(default=35000)
    max_capacity = models.IntegerField(default=300)
    stage = models.BooleanField(default=True)
    lights = models.BooleanField(default=False)
    flowers = models.BooleanField(default=False)
    furniture = models.BooleanField(default=False)
    entrance = models.BooleanField(default=False)
    lounge = models.BooleanField(default=False)

    def __str__(self):
        return self.package_name

class VendorFood(models.Model):
    vendor_name = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, default='CATERER')
    package_name = models.CharField(max_length=120)
    package_price = models.IntegerField(default=50000)
    max_capacity = models.IntegerField(default=300)
    min_value = MaxValueValidator(7,message="Value cannot be more than 7")
    salads = models.SmallIntegerField(default=0, validators=[min_value])
    veg_starter = models.SmallIntegerField(default=0, validators=[min_value])
    veg_main_course = models.SmallIntegerField(default=1, validators=[min_value])
    raita = models.SmallIntegerField(default=0, validators=[min_value])
    dessert = models.SmallIntegerField(default=1, validators=[min_value])
    rotis_bread = models.SmallIntegerField(default=1, validators=[min_value])
    rice_biryani = models.SmallIntegerField(default=1, validators=[min_value])
    dal = models.SmallIntegerField(default=1, validators=[min_value])
    welcome_drinks = models.SmallIntegerField(default=0, validators=[min_value])
    soup = models.SmallIntegerField(default=0, validators=[min_value])
    non_veg_food = models.BooleanField(default=False)
    non_veg_starter = models.SmallIntegerField(default=0, validators=[min_value])
    non_veg_main_course = models.SmallIntegerField(default=0, validators=[min_value])

    def __str__(self):
        return self.package_name


# #---------------------------------------------------------------------------------------------------

class VendorPhotographer(models.Model):
    vendor_name = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, default='DECOR')
    package_name = models.CharField(max_length=120)
    package_price = models.IntegerField(default=25000)
    candid_photo = models.BooleanField(default=False)
    max_value = MaxValueValidator(7,message="Value cannot be more than 7")
    candid_photo_dur = models.SmallIntegerField(default=0,validators=[max_value])
    candid_person = models.SmallIntegerField(default=0,validators=[max_value])
    event_photo = models.BooleanField(default=False)
    event_photo_dur = models.SmallIntegerField(default=0,validators=[max_value])
    event_person = models.SmallIntegerField(default=0,validators=[max_value])
    videography = models.BooleanField(default=False)
    video_dur = models.SmallIntegerField(default=0,validators=[max_value])
    video_person = models.SmallIntegerField(default=0,validators=[max_value])
    main_dur = models.SmallIntegerField(default=0,validators=[max_value])

    def __str__(self):
        return self.package_name

# #---------------------------------------------------------------------------------------------------

class PartArea(models.Model):
    venue_name = models.ForeignKey(UpperVendor, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, default='VENUE')
    area_name = models.CharField(max_length=20)
    seating = models.IntegerField()
    max_capacity = models.IntegerField()
    price = models.IntegerField(default=10000)

    def __str__(self):
        return self.area_name

class VenuePolicy(models.Model):
    min_value = MinValueValidator(0,message="Value cannot be in negative.")
    max_value = MaxValueValidator(100,message="Value cannot be more than 100%")
    policy_name = models.OneToOneField(UpperVendor, on_delete=models.CASCADE)
    venue_decor = models.IntegerField(default=10000, validators=[min_value])
    outside_decor = models.BooleanField(default=False)
    venue_halls_ac = models.BooleanField(default=False)
    venue_room_available = models.BooleanField(default=False)
    venue_room_count = models.IntegerField(default=0, validators=[min_value])
    venue_room_ac = models.IntegerField(default=0, validators=[min_value])
    room_avg_price = models.IntegerField(default=0,validators=[min_value])
    room_ac_avg_price = models.IntegerField(default=0, validators=[min_value])
    changing_room_count = models.IntegerField(default=0, validators=[min_value])
    changing_room_count_ac = models.IntegerField(default=0, validators=[min_value])
    advance_percentage = models.IntegerField(default=25, validators=[max_value, min_value])
    cancellation = models.BooleanField(default=False)
    parking_valet = models.BooleanField(default=False)
    parking_space_count = models.IntegerField(default=10, validators=[min_value])
    alcohol_allowance = models.BooleanField(default=False)
    outside_alcohol = models.BooleanField(default=False)
    music_allowance = models.BooleanField(default=False)
    late_music_allowance = models.BooleanField(default=False)
    firecrackers = models.BooleanField(default=False)
    overnight_function = models.BooleanField(default=False)

    def __str__(self):
        return self.policy_name.vendor_name


#---------------------------------------------------------------------------------------------------