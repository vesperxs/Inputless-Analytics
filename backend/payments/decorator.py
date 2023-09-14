#the decorator
from functools import wraps
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from customers.models import Client
from django_tenants.utils import schema_context
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User

# def admin_only(view_func):
#     def wrap(request, *args, **kwargs):
#         if request.user.profile.userStatus == "admin":
#             return view_func(request, *args, **kwargs)
#         else:
#             return render(request, "dashboard/404.html")
#     return wrap


def checkout(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        get_hostname_from_request = request.get_host().split(':')[0].lower()
        actual_schema = get_hostname_from_request.split('.')[0]
      
        with schema_context(actual_schema):
            tenant_info = Client.objects.all()
            tenant_info_dict = [i for i in tenant_info.values()
                        if i['schema_name'] == actual_schema]
            pk = tenant_info_dict[0]['id']
            tenant = Client.objects.get(pk=pk)
            #print(tenant)
        
            if tenant.is_paid or tenant.type == 'demo':
                Client.objects.filter(pk=pk).update(on_trial=True)
                return render(request,'index.html')
            else:
                return redirect('checkout')

    return wrap

            
