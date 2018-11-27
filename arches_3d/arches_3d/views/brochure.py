import urllib2
from urlparse import urlparse
from django.shortcuts import render
from arches.app.models.system_settings import settings
from django.http import HttpResponseNotFound, HttpResponse

def team(request):
    return render(request, 'team.htm', {
        'main_script': 'team',
        'active_page': 'Team',
        'app_title': settings.APP_TITLE,
        'copyright_text': settings.COPYRIGHT_TEXT,
        'copyright_year': settings.COPYRIGHT_YEAR
    })

def equipment(request):
    return render(request, 'equipment.htm', {
        'main_script': 'equipment',
        'active_page': 'Equipment',
        'app_title': settings.APP_TITLE,
        'copyright_text': settings.COPYRIGHT_TEXT,
        'copyright_year': settings.COPYRIGHT_YEAR
    })
