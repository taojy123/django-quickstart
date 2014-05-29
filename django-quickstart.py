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
outstr = """
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *
import os
import uuid
def index(request):
    return render_to_response('index.html', locals())
#====================login=============================================
def login(request):
    username = request.REQUEST.get('username', '')
    password = request.REQUEST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
    return HttpResponseRedirect("/admin/")

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/admin/")
#======================================================================
"""
open(pname + "/views.py", "w").write(outstr)


#create models
outstr = """
# -*- coding: utf-8 -*-
from django.db import models
class Info(models.Model):
    uid = models.CharField(max_length=64, blank=True , null=True)
    key = models.CharField(max_length=64, blank=True , null=True)
    value = models.CharField(max_length=255, blank=True , null=True)
"""
open(pname + "/models.py", "w").write(outstr)


#modify urls
outstr = """
from django.conf.urls import patterns, include, url
from views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xxx.views.home', name='home'),
    # url(r'^xxx/', include('xxx.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    ('^$', index),
    ('^index/$', index),
)
# This will work if DEBUG is True
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
"""
open(pname + "/urls.py", "w").write(outstr)




#modify settings
outstr = """
# Django settings for %s project.
import os
import uuid

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.getcwd(), 'static').replace('\\\\','/').decode("gbk"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mc8iwu&amp;l9l**d-qcu5)l02woe^7@44t#(&amp;2p85bw)+mrp#y6zn-%s'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

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

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.getcwd(), 'templates').replace('\\\\','/').decode("gbk"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
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
os.chdir(path)  # using pyinstaller to comment it
sys.path.append(path)
print os.getcwd()

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


#modify manage
outstr = """
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
""" % pname
open("manage.py", "w").write(outstr)



#creat run
outstr ="""
#!/usr/bin/env python
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

import django.contrib.auth
import django.contrib.contenttypes
import django.contrib.sessions
import django.contrib.sites
import django.contrib.admin

import django.db.models.sql.compiler
from django.contrib.auth.backends import *
from django.conf.urls.defaults import *
#these are django imports
import django.template.loaders.filesystem
import django.template.loaders.app_directories
import django.middleware.common
import django.contrib.sessions.middleware
import django.contrib.auth.middleware
import django.middleware.doc
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
import django.contrib.messages.models
import django.contrib.staticfiles.models
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
from django.conf.urls.defaults import *
import django.contrib.admin.views.main
import django.core.context_processors
import django.contrib.auth.views
import django.contrib.auth.backends
import django.views.static
import django.contrib.admin.templatetags.log
import django.contrib.admin.templatetags.adminmedia
import django.conf.urls.shortcut
import django.views.defaults
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler
from django.conf import settings
from django.utils import translation
import django.contrib.staticfiles.urls

if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv.append("runserver")
        sys.argv.append("0.0.0.0:8000")
    else:
        webbrowser.open_new_tab('http://127.0.0.1:8000')
    print sys.argv
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



print "Finish!"

raw_input("Press any key to exit...")


