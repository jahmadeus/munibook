"""List of all acceptable url paths. Each url calls an command from the system"""
from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='Index'),
    url(r'^addroutecomment', 'muni.views.addroutecomment',
            name='addroutecomment_json'),
    url(r'^getroutecomments', 'muni.views.getroutecomments',
            name='getroutecomments_json'),
    url(r'^addvehiclecomment', 'muni.views.addvehiclecomment',
            name='addvehiclecomment_json'),
    url(r'^getvehiclecomments', 'muni.views.getvehiclecomments',
            name='getvehiclecomments_json'),
    url(r'^getvehicles', 'muni.views.getvehicles', name='getvehicles_json'),
    url(r'^getvehicle', 'muni.views.getvehicle', name='getvehicle_json'),
    url(r'^getpredictions', 'muni.views.getpredictions',
            name='getpredictions_json'),
    url(r'^getdirections', 'muni.views.getdirections',
            name='getdirections_json'),
    url(r'^getstops$', 'muni.views.getstops', name='getstops_json'),
    url(r'^routes/$', 'muni.views.getRoutes', name='Routes'),
    url(r'^stops/(?P<route>[a-zA-Z0-9_]+)/$', 'muni.views.getStops',
            name='Stops'),
    url(r'^getPredictions/(?P<route>[a-zA-Z0-9_]+)/(?P<stop>[a-zA-Z0-9_]+)/$',
            'muni.views.getPredictions', name='Predictions'),
]
