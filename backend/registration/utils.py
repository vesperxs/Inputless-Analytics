from django_tenants.utils import tenant_context
import datetime
from customers.models import Client, Domain
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
import logging
logger = logging.getLogger(__name__)


def create_user(client, all_data_cleaned):

    # handle exception
    with tenant_context(client):
        user = User()
        user.username = all_data_cleaned['username']
        user.first_name = all_data_cleaned['first_name']
        user.last_name = all_data_cleaned['last_name']
        user.email = all_data_cleaned['email']
        user.set_password(all_data_cleaned['password'])
        user.is_active = True
        user.is_staff = True

        
        user.save()
        logger.debug("[+] Tenant Created")


def create_tenant(all_data_cleaned):

    tenant = Client(
        schema_name= all_data_cleaned['organization'].split('.')[0],
        type=all_data_cleaned['tenant_type'],
        name=all_data_cleaned['organization'].split('.')[0], # remember to remove this
        paid_until='3000-12-05',
        on_trial=True,
        url = 'http://' + all_data_cleaned['organization'],
        created_on=datetime.date.today(),
        arango_db=all_data_cleaned['organization'].split('.')[0],
        organization = all_data_cleaned['organization'].split('.')[0],
        location = all_data_cleaned['city'],
        phone = all_data_cleaned['phone'],
        tenant_email = all_data_cleaned['email'],
    )

    tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!

    # TODO: check if domain is already taken
    domain = Domain()
    domain.domain = all_data_cleaned['organization']# don't add your port or www here!
    domain.tenant = tenant
    domain.is_primary = True
    domain.save()

    return tenant


