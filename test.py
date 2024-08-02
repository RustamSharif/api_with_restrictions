import os
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path

def test_view(request):
    return HttpResponse("Test view works!")

urlpatterns = [
    path('test/', test_view),
]

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_with_restrictions.settings')
    execute_from_command_line(['manage.py', 'runserver', '8001'])