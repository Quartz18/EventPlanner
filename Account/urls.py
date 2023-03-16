from django.contrib import admin
from django.urls import path

from .views import (home_view,
    register_view,
    register_user,
    vendor_register_view,
    register_vendor,
    login_view,
    logout_view,
    city_list_view,
    general_list_view,
    vendor_list_view,
    category_view,
    category_list_view,
    category_city_view,
    general_city_view,
    vendor_profile_detail)

urlpatterns = [
    path('', home_view, name = "home_page"),
    path('Register/',register_view, name="register_page"),
    path('Registered/',register_user, name="registered_user"),
    path('Register/Vendor/', vendor_register_view, name="vendor_register_page"),
    path('Registered/Vendor/', register_vendor, name = "registered_vendor"),
    path('login/',login_view, name ="login_page"),
    path('logout/',logout_view,name="logout_page"),
    path('city/', city_list_view, name = 'city_view'),
    path('general/<str:category>/',general_list_view, name="general_view"),
    path('<int:city_id>/',vendor_list_view, name="vendor_list_view"),
    path('category/<str:category>/', category_view, name = "category_page"),
    path('categorylist/', category_list_view, name = "category_list"),
    path('category/<str:category>/<int:city_id>/', category_city_view, name = "category_city_view"),
    path('citylist/<int:city_id>/',general_city_view, name="general_city_view"),
    path('details/<str:vendor_name>/', vendor_profile_detail, name="vendor_profile_details"),
]