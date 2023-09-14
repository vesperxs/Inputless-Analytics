# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from customers.models import Client
from django_tenants.utils import schema_context
from payments.decorator import checkout





@login_required()
@checkout
def index(request): pass


@login_required()
def search_options(request): 
    return render(request, "search_options.html")
    
@login_required()
def filters(request): 
    return render(request, "filters.html")

@login_required()
def progress_bar_upload(request):
    return render(request, "progress_bar_upload/index.html")

@login_required()
def search(request):
    return render(request, "search/search.html")



@login_required()
def table(request):
    return render(request, "table.html")

@login_required()
def user(request):
    return render(request, "user-profile.html")




@login_required()
def pages(request):

    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))

