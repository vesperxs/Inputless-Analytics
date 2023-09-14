from django.core.management.base import BaseCommand, CommandError
from tenant_users.tenants.utils import create_public_tenant
from tenant_users.tenants.models import ExistsError



class Command(BaseCommand):

    help = "Create Public Tenant"
    
    def add_arguments(self, parser):

        parser.add_argument('--domain', type=str, nargs='?', default="inputless.localhost")
        parser.add_argument('--email',  type=str, nargs='?', default="fake@inputless.com")

    def handle(self, *args, **options):
        # ... call your script here ...
        try:
            create_public_tenant(options['domain'], options['email'])
            self.stdout.write(self.style.SUCCESS('[+] PUBLIC TENANT CREATED'), ending='\n')
            self.stdout.write(self.style.SUCCESS(options))

        except ExistsError:
            self.stdout.write(self.style.ERROR('[-] PUBLIC TENANT ALREADY EXISTS'), ending='\n')
