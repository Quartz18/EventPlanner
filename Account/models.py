from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
#------------------------------------------------------------------------------------------------
class User(AbstractUser):
    class Types(models.TextChoices):
        CLIENT = "CLIENT"
        VENDOR = "VENDOR"
    type = models.CharField(_('Type'),max_length=50,choices=Types.choices, default=Types.CLIENT)

    #First Name and Last Name Do  not Cover Name Patterns
    #Around the globe

    #name = models.CharField(_('Name of User'), blank=True, max_length=255)
    #email = models.EmailField(_('email address main'),unique=True)

    #USERNAME_FIELD = 'email'
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username":self.username})

class ClientManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.CLIENT)

class VendorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.VENDOR)

class Client(User):
    base_type = User.Types.CLIENT
    objects = ClientManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CLIENT
        return super().save(*args,**kwargs)

class Vendor(User):
    base_type = User.Types.VENDOR
    objects = VendorManager()
    class Meta:
        proxy = True

    @property
    def more(self):
        return self.vendormore

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.VENDOR
        return super().save(*args,**kwargs)

class VendorMore(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_regrex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone No. must be entered in the format +919999999999.")
    phone = models.CharField('Phone', validators=[phone_regrex], max_length=12, unique=True,null=True)
#Shell Command:
#Client.objects.create(username="Dilsa",email="dilsadavis@gmail.com"m,type=User.Types.CLIENT)

#------------------------------------------------------------------------------------------------

class Country(models.Model):
    c_name = models.CharField(max_length=100)
    c_log = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.c_name

#-------------------------------------------------------------------------------------------

class City(models.Model):
    city_name = models.CharField(max_length=120)
    c = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_log = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city_name

#-------------------------------------------------------------------------------------------------------