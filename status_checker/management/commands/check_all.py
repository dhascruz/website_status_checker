from django.core.management.base import BaseCommand



from status_checker.views import *



class Command(BaseCommand):
    help = 'Run my custom function'

    def handle(self, *args, **kwargs):
        check_all_websites()  # Call your function
        self.stdout.write('Function executed successfully.')
