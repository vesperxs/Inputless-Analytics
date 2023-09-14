# Create your views here.

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .tasks import init_extraction_task, init_analyze_task, init_save_chart_data, init_calculate_folder_quotas 
from .forms import PhotoForm
from .models import Photo
from celery import current_app
from time import sleep
import os
import subprocess
from django_tenants.utils import schema_context
from django.contrib.admin.views.decorators import staff_member_required
from ratelimit.decorators import ratelimit



class ProgressBarUploadView(View):
    
    @method_decorator(login_required)
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'progress_bar_upload/index.html', {'photos': photos_list})


    @method_decorator(login_required)
    def post(self, request):
        sleep(0.3)

        form = PhotoForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            photo = form.save()
            # print(filename, file)
            data = {
                'is_valid': True,
                'path': photo.file.path,
                'name': photo.file.name,
                'url': photo.file.url
            }
            #upload documents
            upload_task = init_extraction_task.delay(photo.file.path)
            #print(f'Upload Task ID: {upload_task.task_id}')

            # update and store the number of files uploaded
            n_file_uploaded = init_save_chart_data.delay(Photo.objects.all().count())
            #print(f'Counter Task ID: {n_file_uploaded.task_id}')

            # calculate tenant's quotas
            n_folder = init_calculate_folder_quotas.delay(photo.file.path)

        else:
            data = {'is_valid': False}
        return JsonResponse(data)

    

@login_required 
@staff_member_required
def analyze(request):
    if request.method == 'POST':
    #call celery task
        result = init_analyze_task.delay()
    return render(request, 'display_progress.html', context={'task_id': result.task_id})


@login_required
@staff_member_required
def reindex(request):
    if request.method== 'POST':

        get_hostname_from_request = request.get_host().split(':')[0].lower()
        actual_tenant = get_hostname_from_request.split('.')[0]
        with schema_context(actual_tenant):
            path = os.getcwd()
            command = "./manage.py tenant_command rebuild_index --noinput --schema={}".format(actual_tenant)

            process = subprocess.Popen(command,
                shell=True,
                cwd=path) 

        return redirect('home')


@login_required
@staff_member_required

def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))

# @login_required
# class TaskView(View):
#     def get(self, request, task_id):
#         task = current_app.AsyncResult(task_id)
#         response_data = {'task_status': task.status, 'task_id': task.id}

#         if task.status == 'SUCCESS':
#             response_data['results'] = task.get()
#             # print(response_data)

#         return JsonResponse(response_data)
