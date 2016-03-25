from rest_framework import serializers
from models import *

class NavAidSerializer(serializers.ModelSerializer):
    lat = serializers.Field(source="lat")
    lon = serializers.Field(source="lon")

    class Meta:
        model = NavAid
        fields = ('color', 'elevation', 'height', 'lat', 'lon', 'name', 'notes',
         'status', 'sub_type', 'special_category', 'vertical_length')

    def to_native(self, obj):
        '''
        override to not serialize null values
        '''
        ret = self._dict_class()
        ret.fields = {}

        for field_name, field in self.fields.items():
            field.initialize(parent=self, field_name=field_name)
            key = self.get_field_key(field_name)
            value = field.field_to_native(obj, field_name)
            if value is not None:
                ret[key] = value
                ret.fields[key] = field
        return ret


class BeaconSerializer(NavAidSerializer):
    class Meta:
        fields = ('color', 'elevation', 'height', 'lat', 'lon', 'name', 'notes',
         'status', 'sub_type', 'special_category', 'vertical_length', 'shape')
        model = Beacon


class BuoySerializer(NavAidSerializer):
    class Meta:
        fields = ('color', 'elevation', 'height', 'lat', 'lon', 'name', 'notes',
         'status', 'sub_type', 'special_category', 'vertical_length', 'shape', 'color_patern')
        model = Buoy


class DayMarkerSerializer(NavAidSerializer):
    class Meta:
        fields = ('color', 'elevation', 'height', 'lat', 'lon', 'name', 'notes',
         'status', 'sub_type', 'special_category', 'vertical_length', 'top_shape')
        model = DayMarker


class LightSerializer(NavAidSerializer):
    class Meta:
        fields = ('color', 'elevation', 'height', 'lat', 'lon', 'name', 'notes',
         'status', 'sub_type', 'special_category', 'vertical_length', 'characteristic', 
         'exhibition_condition', 'nominal_range', 'orientation', 'signal_group', 
         'signal_period', 'signal_sequence', 'visibility')
        model = Light


class MooringSerializer(NavAidSerializer):
    class Meta:
        fields = ('color', 'elevation', 'height', 'lat', 'lon', 'name', 'notes',
         'status', 'special_category', 'vertical_length', 'water_level')
        model = Mooring

