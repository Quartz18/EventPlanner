from django.contrib import admin
from django.urls import path

from .views import (vendor_home_view,
    profile_view,
    vendor_basic_form_view,
    vendor_profile_detail,
    edit_time_form,
    edit_image_form,
    edit_address_form,
    edit_contact_form,
    edit_policy_form,
    edit_party_form,
    edit_food_form,
    edit_decor_form,
    edit_photographer_form,
    edit_name_form,
    vendor_detail,
    category_view,
    schedule_meeting_list,
    pending_schedule,
    canceling_schedule,
    getFoodDetails,
    getDecorDetails,
    getPhotographerDetails,
    deleteService,
    testing)

urlpatterns = [
    path('', vendor_home_view, name = "vendor_main_page"),
    path('u/',profile_view, name="vendor_profile_page"),
    path('venueform/',vendor_basic_form_view, name="venue_basic_form"),
    path('vendor/<str:vendor_name>/',vendor_profile_detail, name="vendor_profile_edit"),
    path('time/',edit_time_form, name="edit_time_form"),
    path('image/',edit_image_form, name="edit_image_form"),
    path('address/',edit_address_form, name="edit_address_form"),
    path('contact/',edit_contact_form, name="edit_contact_form"),
    path('policy/',edit_policy_form, name="edit_policy_form"),
    path('party/',edit_party_form, name="edit_party_form"),
    path('food/',edit_food_form, name="edit_food_form"),
    path('decor/',edit_decor_form, name="edit_decor_form"),
    path('photographer/',edit_photographer_form, name="edit_photographer_form"),
    path('name/',edit_name_form, name="edit_name_form"),
    path('details/<str:vendor_name>/',vendor_detail, name="vendor_details_vendor"),
    path('category/<str:category>/', category_view, name = "vendor_category_page"),
    path('schedulelist/', schedule_meeting_list, name="schedule_meeting_list"),
    path('testing/', testing, name="testing"),
    path('pendingschedule/', pending_schedule, name="pending_schedule"),
    path('cancelingschedule/', canceling_schedule, name="canceling_schedule"),
    path('foodDetail/<str:package_id>/', getFoodDetails, name="FoodDetail"),
    path('decorDetail/<str:package_id>/', getDecorDetails, name="DecorDetail"),
    path('photographerDetail/<str:package_id>/', getPhotographerDetails, name="PhotographerDetails"),
    path('delete/service>/', deleteService, name="deleteService"),
]