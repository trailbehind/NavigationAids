from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import *

nav_aid_api_patterns = patterns('chartTracker.navAids.views',
    url(r'^$', 'api_root'),
    url(r'^beacon/$', BeaconList.as_view(), name='beacon-list'),
    url(r'^beacon/(?P<pk>[\w\.]+)/$', BeaconDetail.as_view(), name='beacon-detail'),
    url(r'^buoy/$', BuoyList.as_view(), name='buoy-list'),
    url(r'^buoy/(?P<pk>[\w\.]+)/$', BuoyDetail.as_view(), name='buoy-detail'),
    url(r'^daymarker/$', DayMarkerList.as_view(), name='daymarker-list'),
    url(r'^daymarker/(?P<pk>[\w\.]+)/$', DayMarkerDetail.as_view(), name='daymarker-detail'),
    url(r'^light/$', LightList.as_view(), name='light-list'),
    url(r'^light/(?P<pk>[\w\.]+)/$', LightDetail.as_view(), name='light-detail'),
    url(r'^mooring/$', MooringList.as_view(), name='mooring-list'),
    url(r'^mooring/(?P<pk>[\w\.]+)/$', MooringDetail.as_view(), name='mooring-detail'),
)

urlpatterns = format_suffix_patterns(nav_aid_api_patterns, allowed=['json', 'api'])
