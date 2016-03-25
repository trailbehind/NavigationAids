from django.contrib.gis.db import models
from django.contrib.gis.geos.point import Point

color_map = ("Unknown", "white", "black", "red", "green", "blue", "yellow", "grey", "brown", "amber", "violet", "orange", "magenta", "pink")

class NavAid(models.Model):
    color = models.CharField(max_length=100, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    elevation = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    location = models.PointField(dim=2)
    name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    scale_max = models.IntegerField(blank=True, null=True)
    scale_min = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(default=1)
    sub_type = models.CharField(max_length=100, blank=True, null=True)
    special_category = models.CharField(max_length=100, blank=True, null=True)
    vertical_length = models.IntegerField(blank=True, null=True)

    objects = models.GeoManager()


    class Meta:
        abstract = True


    @classmethod
    def create_or_update(cls, feature, geom):
        obj = None

        if not obj:
            obj = cls()

        if 'COLOUR' in feature.fields:
            obj.color = feature.get('COLOUR')
        if 'ELEVAT' in feature.fields:
            obj.elevation = feature.get('ELEVAT')
        if 'HEIGHT' in feature.fields:
            obj.height = feature.get('HEIGHT')
        if 'OBJNAM' in feature.fields:
            try:
                obj.name = feature['OBJNAM'].as_string()
            except Exception, e:
                print e
        if 'INFORM' in feature.fields:
            try:
                obj.notes = feature['INFORM'].as_string()
            except Exception, e:
                print e
        if 'SCAMIN' in feature.fields:
            obj.scale_min = feature.get('SCAMIN')
        if 'SCAMAX' in feature.fields:
            obj.scale_max = feature.get('SCAMAX')
        if 'STATUS' in feature.fields:
            obj.status = feature.get('STATUS')
        if 'VERLEN' in feature.fields:
            obj.vertical_length = feature.get('VERLEN')

        obj.location = Point(geom.x, geom.y)

        return obj


    def color_name(self):
        if self.color is None:
            return None

        colors = string.split(self.color, ',')
        color_strings = []
        for color in colors:
            color_strings.append(color_map[color])

        return ','.join(color_strings)


    def lat(self):
        return self.location.y


    def lon(self):
        return self.location.x


    def type_name(self):
        return 'NavAid'


    def __unicode__(self):
        return self.name


class Beacon(NavAid):
    shape = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def create_or_update(cls, feature, geom):
        obj = super(Beacon, cls).create_or_update(feature, geom)

        if 'BCNSHP' in feature.fields:
            obj.shape = feature.get('BCNSHP')

        return obj


    def type_name(self):
        return 'Beacon'


class Buoy(NavAid):
    shape = models.CharField(max_length=100, blank=True, null=True)
    color_patern = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def create_or_update(cls, feature, geom):
        obj = super(Buoy, cls).create_or_update(feature, geom)

        if 'BOYSHP' in feature.fields:
            obj.shape = feature.get('BOYSHP')
        if 'COLPAT' in feature.fields and len(feature.get('COLPAT')) > 0:
            obj.color_patern = feature.get('COLPAT')

        return obj


    def type_name(self):
        return 'Buoy'


class DayMarker(NavAid):
    top_shape = models.IntegerField(blank=True, null=True)

    @classmethod
    def create_or_update(cls, feature, geom):
        obj = super(DayMarker, cls).create_or_update(feature, geom)

        if 'TOPSHP' in feature.fields:
            obj.top_shape = feature.get('TOPSHP')

        return obj


    def type_name(self):
        return 'DayMarker'


class Light(NavAid):
    characteristic = models.IntegerField(blank=True, null=True)
    exhibition_condition = models.IntegerField(blank=True, null=True)
    nominal_range = models.IntegerField(blank=True, null=True)
    orientation = models.FloatField(blank=True, null=True)
    signal_group = models.CharField(max_length=100, blank=True, null=True)
    signal_period = models.FloatField(blank=True, null=True)
    signal_sequence = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.IntegerField(blank=True, null=True)

    @classmethod
    def create_or_update(cls, feature, geom):
        obj = super(Light, cls).create_or_update(feature, geom)

        if 'CATLIT' in feature.fields:
            obj.special_category = feature.get('CATLIT')
        if 'EXCLIT' in feature.fields:
            obj.exhibition_condition = feature.get('EXCLIT')
        if 'LITCHR' in feature.fields:
            obj.characteristic = feature.get('LITCHR')
        if 'LITVIS' in feature.fields and len(feature.get('LITVIS')) > 0:
            obj.visibility = feature.get('LITVIS')
        if 'ORIENT' in feature.fields:
            obj.orientation = feature.get('ORIENT')
        if 'SIGGRP' in feature.fields:
            obj.signal_group = feature.get('SIGGRP')
        if 'SIGPER' in feature.fields:
            obj.signal_period = feature.get('SIGPER')
        if 'SIGSEQ' in feature.fields:
            obj.signal_sequence = feature.get('SIGSEQ')

        return obj


    def type_name(self):
        return 'Light'


class Mooring(NavAid):
    water_level = models.IntegerField(blank=True, null=True)

    @classmethod
    def create_or_update(cls, feature, geom):
        obj = super(Mooring, cls).create_or_update(feature, geom)

        if 'WATLEV' in feature.fields:
            obj.water_level = feature.get('WATLEV')

        return obj


    def type_name(self):
        return 'Mooring'


