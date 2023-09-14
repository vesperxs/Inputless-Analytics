from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from customers.models import Client

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('name','schema_name','paid_until')




"""
from django.contrib import admin
from django.apps import apps
from django_tenants.utils import get_public_schema_name

class TenantsAdmin(admin.ModelAdmin):
    '''
    Hides public models from tenants
    '''
    def has_view_permission(self,request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
    def has_add_permission(self,request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
    def has_change_permission(self,request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
    def has_delete_permission(self,request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
    def has_view_or_change_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
app = apps.get_app_config('tenants')
for model_name, model in app.models.items():
    admin.site.register(model, TenantsAdmin)
"""