from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if(request.user.is_authenticated):
            if(request.user.type == 'VENDOR'):
                return redirect("/Vendor/")
            else:
                return redirect("/u/")
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def authenticated_vendor(view_func):
    def wrapper_func(request, *args, **kwargs):
        if(request.user.is_authenticated):
            if(request.user.type == 'VENDOR'):
                return view_func(request, *args, **kwargs)
            else:
                return redirect("/u/")
        else:
            return redirect("/")
    
    return wrapper_func

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if(request.user.is_authenticated):
            if(request.user.type == 'CLIENT'):
                return view_func(request, *args, **kwargs)
            else:
                return redirect("/Vendor/")
        else:
            return redirect("/")
    
    return wrapper_func

def authenticate_all_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if(request.user == 'AnonymousUser'):
            return redirect("/")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func