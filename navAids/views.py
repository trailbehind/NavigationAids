from models import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from serializers import *
import logging
from rest_framework import renderers
from django.views.generic import TemplateView


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'beacons': reverse('beacon-list', request=request),
        'beacon': reverse('beacon-detail', args=['1'], request=request),
        'buoys': reverse('buoy-list', request=request),
        'buoy': reverse('buoy-detail', args=['1'], request=request),
        'daymarkers': reverse('daymarker-list', request=request),
        'daymarker': reverse('daymarker-detail', args=['1'], request=request),
        'lights': reverse('light-list', request=request),
        'light': reverse('light-detail', args=['1'], request=request),
        'moorings': reverse('mooring-list', request=request),
        'mooring': reverse('mooring-detail', args=['1'], request=request),
    })


class NavAidList(generics.ListAPIView): 
	renderer_classes = (renderers.JSONRenderer,)
	model = NavAid


class NavAidDetail(generics.RetrieveAPIView):
	model = NavAid


class BeaconList(NavAidList):
	renderer_classes = (renderers.JSONRenderer,)
	model = Beacon
	serializer_class = BeaconSerializer


class BeaconDetail(NavAidDetail):
	model = Beacon
	serializer_class = BeaconSerializer


class BuoyList(NavAidList):
	renderer_classes = (renderers.JSONRenderer,)
	model = Buoy
	serializer_class = BuoySerializer


class BuoyDetail(NavAidDetail):
	model = Buoy
	serializer_class = BuoySerializer


class DayMarkerList(NavAidList):
	renderer_classes = (renderers.JSONRenderer,)
	model = DayMarker
	serializer_class = DayMarkerSerializer


class DayMarkerDetail(NavAidDetail):
	model = DayMarker
	serializer_class = DayMarker


class LightList(NavAidList):
	renderer_classes = (renderers.JSONRenderer,)
	model = Light
	serializer_class = LightSerializer


class LightDetail(NavAidDetail):
	model = Light
	serializer_class = LightSerializer


class MooringList(NavAidList):
	renderer_classes = (renderers.JSONRenderer,)
	model = Mooring
	serializer_class = MooringSerializer


class MooringDetail(NavAidDetail):
	model = Mooring
	serializer_class = MooringSerializer

