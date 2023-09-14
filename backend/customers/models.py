from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.utils import get_tenant_type_choices
import uuid
import os

class Client(TenantMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, choices=get_tenant_type_choices())
    url = models.URLField(blank=True, null=True)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(null=True, blank=True)
    is_converted = models.BooleanField(null=True, blank=True)
    arango_db = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=30,blank=True,null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30,blank=True,null=True)
    tenant_email = models.CharField(max_length=30, blank=True, null=True)
    


    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True


    def __str__(self):
        return f"{self.schema_name} - {self.id} - {self.type}"



class Domain(DomainMixin):
    pass
