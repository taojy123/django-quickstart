#coding=utf8

import os
import sys
import uuid

if len(sys.argv) < 2:
    pname = raw_input("The project name:")
else:
    pname = sys.argv[1]

#creat app dir
if not os.path.exists(os.path.join(os.getcwd(), pname)):
    os.makedirs(os.path.join(os.getcwd(), pname))


#create views
outstr = """# -*- coding: utf-8 -*-

import StringIO
import HTMLParser
import BeautifulSoup
import xlwt

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *


def index(request):
    return render_to_response('index.html', locals())

@login_required
def reminders(request):
    reminders = Reminder.objects.all().order_by('-id')
    return render_to_response('reminders.html', locals())


@login_required
def reminder(request, reminder_id):

    if reminder_id == 'add':
        reminder = Reminder()
    else:
        reminder = get_object_or_404(Reminder, id=reminder_id)

    is_new = not reminder.id

    if request.method == 'POST':
        name = request.POST.get('name')
        method = request.POST.get('method')
        ahead_hours = request.POST.get('ahead_hours')
        enable = request.POST.get('enable', False)

        reminder.name = name
        reminder.method = method
        reminder.ahead_hours = ahead_hours
        reminder.enable = enable
        reminder.save()

        return HttpResponseRedirect('/reminders/')

    return render_to_response('reminder.html', locals())


@login_required
def reminder_delete(request, reminder_id):
    Reminder.objects.filter(id=reminder_id).delete()
    return HttpResponseRedirect('/reminders/')


def login(request):
    msg = ''
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_url = request.POST.get('next', '/')
        user = auth.authenticate(username=username, password=password)
        print(username, password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            msg = u'username or password error'
    return render_to_response('login.html', locals())


def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/")


@login_required
def password(request):
    msg = ''
    if request.method == 'POST':
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        user = request.user

        if not user.check_password(password):
            msg = u'old password error'

        if password1 != password2:
            msg = u'two passwords not the same'

        if not msg:
            user.set_password(password1)
            user.save()
            return HttpResponseRedirect('/login/')

    return render_to_response('password.html', locals())


def output(request):
    data = request.POST.get('data')
    begin_index = int(request.POST.get('begin_index', 0))
    end_index = int(request.POST.get('end_index', 999))

    html_parser = HTMLParser.HTMLParser()

    wb = xlwt.Workbook()
    ws = wb.add_sheet('output')

    soup = BeautifulSoup.BeautifulSoup(data)

    thead_soup = soup.find('thead')
    th_soups = thead_soup.findAll(['th', 'td'])
    th_soups = th_soups[begin_index:end_index]

    j = 0
    for th_soup in th_soups:
        th = th_soup.getText()
        th = html_parser.unescape(th).strip()
        ws.write(0, j, th)
        j += 1

    tbody_soup = soup.find('tbody')
    tr_soups = tbody_soup.findAll('tr')

    i = 1
    for tr_soup in tr_soups:
        td_soups = tr_soup.findAll(['td', 'th'])
        td_soups = td_soups[begin_index:end_index]

        j = 0
        for td_soup in td_soups:
            td = td_soup.getText()
            td = html_parser.unescape(td).strip()
            ws.write(i, j, td)
            j += 1

        i += 1

    s = StringIO.StringIO()
    wb.save(s)
    s.seek(0)
    data = s.read()
    response = HttpResponse(data)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="output.xls"'

    return response
"""
open(pname + "/views.py", "w").write(outstr)


#create models
outstr = """# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Reminder(models.Model):

    METHOD_CHOICES = (
        (1, 'Email'),
        (2, 'SMS'),
    )
    name = models.CharField(max_length=255, blank=True)
    method = models.IntegerField(choices=METHOD_CHOICES, default=1)
    ahead_hours = models.IntegerField(default=24)
    enable = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(default=timezone.now)
"""
open(pname + "/models.py", "w").write(outstr)


#create admin
outstr = """
from collections import OrderedDict

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils.text import capfirst


from models import *


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse
    return inner


registry = OrderedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)
admin.site.site_header = 'XXX'

admin.site.unregister(Group)
admin.site.unregister(Site)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ['id', 'action_time', 'user', '__str__']
    readonly_fields = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message', 'objects']

"""
open(pname + "/admin.py", "w").write(outstr)


#modify urls
outstr = '''
"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin

from views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', index),
    url(r'^index/$', index),

    url(r'^reminders/$', reminders),
    url(r'^reminders/(\d+|add)/$', reminder),
    url(r'^reminders/(\d+)/delete/$', reminder_delete),
    
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^password/$', password),

    url(r'^output/$', output),
]


# This will work if DEBUG is True
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

# This will work if DEBUG is True or False
# from django.conf import settings
# from django.views.static import serve
# import re
# urlpatterns.append(url(
#     '^' + re.escape(settings.STATIC_URL.lstrip('/')) + '(?P<path>.*)$',
#     serve,
#     {'document_root': './static/'}))
'''
open(pname + "/urls.py", "w").write(outstr)




#modify settings
outstr = """
# coding=utf-8
# Django settings for %s project.
import os
import uuid

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

LOGIN_URL = '/login/'

ALLOWED_HOSTS = ['*']

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'data.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        # 'OPTIONS': {'charset': 'utf8mb4'}, # for emoji at mysql
    }
}

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# USE_L10N must be False, below will work
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i'
# DATE_FORMAT = 'j E Y r.'
# TIME_FORMAT = 'G:i'
# DATETIME_FORMAT = 'j E Y г. G:i'
# YEAR_MONTH_FORMAT = 'F Y г.'
# MONTH_DAY_FORMAT = 'j F'
# SHORT_DATE_FORMAT = 'd.m.Y'
# SHORT_DATETIME_FORMAT = 'd.m.Y H:i'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_URL = '/static/'


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = './static/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/static/media/'


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'django-quickstart-%s'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '%s.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '%s.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    '%s',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


SERVER_EMAIL = 'watchmen123456@163.com'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'watchmen123456'
EMAIL_HOST_PASSWORD = 'wm123456'


""" % (pname, str(uuid.uuid4()),pname, pname, pname)
open(pname + "/settings.py", "w").write(outstr)



#modify wsgi
outstr = '''
"""
WSGI config for %s project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

path = os.path.dirname(__file__)
path = os.path.join(path, "..")
#os.chdir(path)  # using web server for deploy to uncomment it
sys.path.append(path)
print(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
''' % (pname, pname)
open(pname + "/wsgi.py", "w").write(outstr)


#__init__.py
open(pname + "/__init__.py", "w").write("")


#creat 1.cmd
open("1.cmd", "w").write("cmd")


#creat run.bat
open("run.bat", "w").write("python manage.py runserver 0.0.0.0:8000")


#modify manage
outstr = """#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
""" % pname
open("manage.py", "w").write(outstr)



#creat run
outstr ="""#!/usr/bin/env python

import os
import sys
import webbrowser
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings")
#these pertain to your application
import %s.wsgi
import %s.urls
import %s.settings
import %s.models
import %s.views

import django.contrib.sessions.serializers
import django.contrib.auth
import django.contrib.contenttypes
import django.contrib.sessions
import django.contrib.sites
import django.contrib.admin

import django.db.models.sql.compiler
from django.contrib.auth.backends import *
# from django.conf.urls.defaults import *
#these are django imports
import django.template.loaders.filesystem
import django.template.loaders.app_directories
import django.middleware.common
import django.contrib.sessions.middleware
import django.contrib.auth.middleware
# import django.middleware.doc
import django.contrib.messages
import django.contrib.staticfiles
import django.contrib.messages.middleware
import django.contrib.sessions.backends.db
#import django.contrib.messages.storage.user_messages
import django.contrib.messages.storage.fallback
import django.db.backends.sqlite3.base
import django.db.backends.sqlite3.introspection
import django.db.backends.sqlite3.creation
import django.db.backends.sqlite3.client
import django.contrib.auth.context_processors
from django.core.context_processors import *
import django.contrib.messages.context_processors
import django.contrib.auth.models
import django.contrib.contenttypes.models
import django.contrib.sessions.models
import django.contrib.sites.models
# import django.contrib.messages.models
# import django.contrib.staticfiles.models
import django.contrib.admin.models
import django.template.defaulttags
import django.template.defaultfilters
import django.template.loader_tags
#dont need to import these pkgs
#need to know how to exclude them
import email.mime.audio
import email.mime.base
import email.mime.image
import email.mime.message
import email.mime.multipart
import email.mime.nonmultipart
import email.mime.text
import email.charset
import email.encoders
import email.errors
import email.feedparser
import email.generator
import email.header
import email.iterators
import email.message
import email.parser
import email.utils
import email.base64mime
import email.quoprimime
import django.core.cache.backends.locmem
import django.templatetags.i18n
import django.templatetags.future
import django.views.i18n
import django.core.context_processors
import django.template.defaulttags
import django.template.defaultfilters
import django.template.loader_tags
# from django.conf.urls.defaults import *
import django.contrib.admin.views.main
import django.core.context_processors
import django.contrib.auth.views
import django.contrib.auth.backends
import django.views.static
import django.contrib.admin.templatetags.log
# import django.contrib.admin.templatetags.adminmedia
# import django.conf.urls.shortcut
import django.views.defaults
from django.core.handlers.wsgi import WSGIHandler
# from django.core.servers.basehttp import AdminMediaHandler
from django.conf import settings
from django.utils import translation
import django.contrib.staticfiles.urls

import Cookie
import htmlentitydefs
import HTMLParser

if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv.append("runserver")
        sys.argv.append("0.0.0.0:8000")
    else:
        webbrowser.open_new_tab('http://127.0.0.1:8000')
    print(sys.argv)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

""" % (pname, pname, pname, pname, pname, pname)
open("run.py", "w").write(outstr)


# creat templates dir
if not os.path.exists(os.path.join(os.getcwd(), 'templates')):
    os.makedirs(os.path.join(os.getcwd(), 'templates'))
open("templates/index.html", "w").write("HELLO WORLD")


# creat static dir
if not os.path.exists(os.path.join(os.getcwd(), 'static', 'images')):
    os.makedirs(os.path.join(os.getcwd(), 'static', 'images'))
if not os.path.exists(os.path.join(os.getcwd(), 'static', 'js')):
    os.makedirs(os.path.join(os.getcwd(), 'static', 'js'))
if not os.path.exists(os.path.join(os.getcwd(), 'static', 'css')):
    os.makedirs(os.path.join(os.getcwd(), 'static', 'css'))


#create uwsgi config
outstr = """[uwsgi]
chdir=./
wsgi-file=./%s/wsgi.py
master=True
processes=2
threads=2
http-socket=0.0.0.0:8000
daemonize=/var/log/uwsgi/%s.log
pidfile=/tmp/%s.pid
#socket=127.0.0.1:8000
#virtualenv=/root/envdj16
#stats=0.0.0.0:18000
""" % (pname, pname, pname)
open("uwsgi_%s.ini" % pname, "w").write(outstr)


#create requirement
outstr = """django
xlwt
BeautifulSoup
"""
open("requirement.txt", "w").write(outstr)


print("Finish!")

raw_input("Press any key to exit...")


