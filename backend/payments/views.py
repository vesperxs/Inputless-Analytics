from re import TEMPLATE
from typing import Any
import json
import stripe
import djstripe
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
import os
from django.core.exceptions import ObjectDoesNotExist
import subprocess
from django_tenants.utils import schema_context
from django.db import connection
from django.contrib.auth.models import User
# Create your views here.
from djstripe.models import Product, Customer
from django.contrib.auth.decorators import login_required
from customers.models import Client
from accounts.models import CustomerProfile
from django.core.mail import send_mail, BadHeaderError

@login_required()
def checkout(request):
    products = Product.objects.all()
    return render(request,"checkout.html", {"products": products})


@login_required()
def create_sub(request):
  if request.method == 'POST':
	  	
      # Reads application/json and returns a response
      data = json.loads(request.body)

      payment_method = data['payment_method']
      stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

      payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
      djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)


      try:
          # This creates a new Customer and attaches the PaymentMethod in one API call.
          customer = stripe.Customer.create(
              payment_method=payment_method,
              email=request.user.email,
              invoice_settings={
                  'default_payment_method': payment_method
              }
          )
          djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
          request.user.customer = djstripe_customer
         

          # At this point, associate the ID of the Customer object with your
          # own internal representation of a customer, if you have one.
          # print(customer) 
          user = User.objects.get(pk=1)
          customer_obj = CustomerProfile()
          customer_obj.user = user
          customer_obj.customer = djstripe_customer
          
          ############################################################################ 

          # Subscribe the user to the subscription created
          subscription = stripe.Subscription.create(
              customer=customer.id,
              items=[
                  {
                      "price": data["price_id"],
                  },
              ],
              expand=["latest_invoice.payment_intent"]
          )

          djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

          request.user.subscription = djstripe_subscription
          
          # save the subscription_id with own internal rappresentation

          customer_obj.subscription = djstripe_subscription
          ########################################################################

          customer_obj.save()
          request.user.save()

          return JsonResponse(subscription)
      except Exception as e:
          return JsonResponse({'error': (e.args[0])}, status =403)
  else:
      return HttpResponse('request method not allowed')

      
      

@login_required()
def complete(request):
    # confim if user has paid
    get_hostname_from_request = request.get_host().split(':')[0].lower()
    actual_schema = get_hostname_from_request.split('.')[0]
    with schema_context(actual_schema):

        tenant_info = Client.objects.all()
        tenant_info_dict = [i for i in tenant_info.values()
                        if i['schema_name'] == actual_schema]
        pk = tenant_info_dict[0]['id']
        # transform demo to professional mode
        if tenant_info_dict[0]['type'] == 'demo':
            Client.objects.filter(pk=pk).update(
                type="professional",
                is_converted=True,
                is_paid=True,
                on_trial=False
            )
            
    return render(request, "payment_confirmed.html")

@login_required
def billing_view(request):
    get_hostname_from_request = request.get_host().split(':')[0].lower()
    actual_schema = get_hostname_from_request.split('.')[0]
    with schema_context(actual_schema):
        tenant_info = Client.objects.all()
        tenant_info_dict = [i for i in tenant_info.values()
                        if i['schema_name'] == actual_schema]
        pk = tenant_info_dict[0]['id']
        try:
            products = Product.objects.all()
            customer_obj = CustomerProfile.objects.get(pk=1)
            start_sub, end_sub = customer_obj.subscription.current_period_start, \
            customer_obj.subscription.current_period_end
            Client.objects.filter(pk=pk).update(paid_until=end_sub)
            
            return render(request,"user-billing.html",
                          {
                            "products": products,
                            "start_sub":start_sub,
                            "end_sub":end_sub
                          })
        except ObjectDoesNotExist:
            pass
            
    return render(request,"user-billing.html",{
        "products": products,
        "tenant":tenant_info_dict[0]['type']
    }) 

@login_required
def convert(request):
    """ Convert demo account to subscribed user plan """
    
    get_hostname_from_request = request.get_host().split(':')[0].lower()
    actual_schema = get_hostname_from_request.split('.')[0]

    with schema_context(actual_schema):

        tenant_info = Client.objects.all()
        tenant_info_dict = [i for i in tenant_info.values()
                        if i['schema_name'] == actual_schema]
        pk = tenant_info_dict[0]['id']
        tenant = Client.objects.get(pk=pk)
        #print(tenant_info_dict)
        # check if tenant is demo or not
        if tenant.type == "demo":
            return redirect("checkout")
        else:
            return redirect("home")
    

@login_required()
def cancel(request):
    """ Cancel Subscription and tenant """
    
    if request.user.is_authenticated:
        customer_obj = CustomerProfile.objects.get(pk=1)
        sub_id = customer_obj.subscription.id
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        try:
            stripe.Subscription.delete(sub_id)

        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status =403)

        #command = "./manage.py delete_tenant -s {}".format(connection.schema_name)
        #process = subprocess.call(command,shell=True )
        #stdin=subprocess.PIPE, stdout=subprocess.PIPE


    ## redirect to goodbye
    return redirect("home")

