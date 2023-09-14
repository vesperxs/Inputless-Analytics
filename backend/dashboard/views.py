
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from upload.models import ChartInfo
from upload.models import ChartFolderQuotas
from django_tenants.utils import schema_context
from django.contrib.auth.models import User
from upload.models import ChartsNLP
import datetime


@login_required()
def dashboard(request):
    get_hostname_from_request = request.get_host().split(':')[0].lower()
    actual_schema = get_hostname_from_request.split('.')[0]

    data = {
        'tot_month_doc':[],
        'tot_doc':'',
        'tot_user':'',
        'folder_quotas':'',
        'space_limit':'',
    }

    with schema_context(actual_schema):
        # accounted tot doc for 12 month 
        tot_monthly_data = []
        today = datetime.date.today()
        if ChartInfo.objects.filter(created_at__month=today.month).exists():
            queryset = ChartInfo.objects.filter(created_at__month=today.month).last() 
            data['tot_month_doc'].append(queryset.numbers_of_file_uploaded)

        # accounted tot doc uploaded

        if ChartInfo.objects.exists(): 
            tot_doc_uploaded = ChartInfo.objects.last()
            tot = tot_doc_uploaded.numbers_of_file_uploaded
            data['tot_doc'] = tot
        else:
            data['tot_doc'] = 0
        
        # account folder quotas until limiter
        limit = 31457280 #30gb
        if ChartFolderQuotas.objects.exists():
            account_folder_quotas = ChartFolderQuotas.objects.last()
            data['folder_quotas'] = account_folder_quotas.folder_size
            data['space_limit'] = limit
            if int(account_folder_quotas.folder_size) > limit:
                # send an allert email to the user 
                print("block")
        else:
            account_folder_quotas = 0


        # retrieve total user per account
        tot_user = User.objects.all().count()
        data['tot_user'] = tot_user


        #nlp data
        if ChartsNLP.objects.exists():
            data['nlp_data'] = ChartsNLP.objects.values().last()['nlp_data']

        return render(request, "dashboard.html", {
            'chart_data':data
        })

    return render(request, "dashboard.html")
