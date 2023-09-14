from django.core.management.base import BaseCommand, CommandError
from tenant_users.tenants.utils import get_user_model
from tenant_users.tenants.models import ExistsError
from passwordgenerator import pwgenerator


class Command(BaseCommand):

    help = "Create tenant user from object model"
    
    def add_arguments(self, parser):

        parser.add_argument('--email', type=str, required=True)
        parser.add_argument('--password', nargs='?', type=str, default=pwgenerator.generate())
        parser.add_argument('--active', type=bool, default=True)

    def handle(self, *args, **options):
        # ... call your script here ...
        TenantUser = get_user_model()
        try:
            
            user = TenantUser.objects.create_user(email=options['email'],
                                              password=options['password'],
                                              is_active=options['active'])

            self.stdout.write(self.style.SUCCESS('[+] USER CREATED'), ending='\n')
            self.stdout.write(self.style.SUCCESS(options))

        except ExistsError:
            self.stdout.write(self.style.ERROR('[-] USER ALREADY EXISTS'), ending='\n')
