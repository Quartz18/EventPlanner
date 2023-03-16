from django.contrib import admin
from django.urls import path

from .views import (
    user_home_view,
    category_view,
    vendor_detail,
    schedule_meeting,
    cancel_schedule,
    profile_view,
    create_event,
    schedule_list,
    event_list,
    event_details,
    major_event_details,
    eventRequire
)

urlpatterns = [
    path('', user_home_view, name = "user_main_page"),
    path('details/<str:vendor_name>/',vendor_detail, name="vendor_details_client"),
    path('category/<str:category>/', category_view, name = "client_category_page"),
    path('schedule/', schedule_meeting, name = "schedule_meeting_page"),
    path('cancel/', cancel_schedule, name = "cancel_schedule"),
    path('profile/', profile_view, name = "profile_view"),
    path('create/', create_event, name = "create_event"),
    path('schedulelist/', schedule_list, name = "schedule_list"),
    path('eventlist/', event_list, name = "event_list"),
    path('event/<str:event_name>/', event_details, name = "event_details"),
    path('category/event/<str:event_name>/', major_event_details, name = "major_event_details"),
    path('update/event/', eventRequire, name = "eventRequire"),

]