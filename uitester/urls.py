from django.conf.urls.defaults import *
from uitester.settings import INSTALL_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^uitester/', include('uitester.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^$', 'uitester.views.index'),
    (r'^rankings/$', 'uitester.views.rankings'),
    (r'^survey/start/$', 'uitester.views.startSurvey'),
    (r'^survey/(?P<id>[0-9]+)/$', 'uitester.views.surveyPage'),
    (r'^survey/logscore/$', 'uitester.views.logSurveyScores'),
    ### TEMPORARY, REMOVE IN PRODUCTION SITE ###
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/media' % INSTALL_ROOT}),
)
