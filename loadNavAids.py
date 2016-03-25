#!/usr/bin/env python
import sys
from datetime import datetime
from chartTracker import settings
from django.contrib.gis.geos import GEOSGeometry
import os
import logging
from optparse import OptionParser
import itertools
import csv
import re


from django.contrib.gis.gdal import DataSource, CoordTransform, SpatialReference, OGRGeometry
from django.contrib.gis.geos import *

def l_d(*parms):
    #logging.debug(' '.join(itertools.imap(repr,parms)))
    print (' '.join(itertools.imap(repr,parms)))


def getObjectClasses():
    csv_file = 's57objectclasses.csv'
    object_classes = dict()
    with open(csv_file, 'rb') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            code = str(row['Code'])
            class_name = row['ObjectClass']
            if code and class_name:
                object_classes[code] = class_name
    return object_classes


def loadFiles(directory):
    for file_name in os.listdir(directory):
        (root, ext) = os.path.splitext(file_name)
        if ext == ".shp":
            shape_path = os.path.join(directory, file_name)
            loadShapeFile(shape_path)
        else:
            l_d("not opening file", file_name)



def loadShapeFile(path):
    from chartTracker.navAids.models import Beacon, Buoy, DayMarker, Light, Mooring

    TYPE_MAP = dict(
        Beacon=Beacon,
        Buoy=Buoy,
        Daymark=DayMarker,
        Light=Light,
        Mooring=Mooring
    )

    l_d("Opening shapefile %s" % path)
    inputShp = DataSource(path)
    l_d("fields: %s" % inputShp[0].fields)

    object_classes = getObjectClasses()

    for inputLayer in inputShp:
        print('Layer "%s": %i %ss' % (inputLayer.name, len(inputLayer), inputLayer.geom_type.name))
        ct = CoordTransform(inputLayer.srs, SpatialReference('WGS84'))

        for feature in inputLayer:
            feature_class_code = "%.0f" % feature.get("OBJL")
            feature_class_name = object_classes[feature_class_code]
            m = re.search('^(\w+)\W+(.*)$', feature_class_name)
            sub_type_name = None
            if m:
                feature_class_name = m.group(1)
                sub_type_name = m.group(2)

            feature_class = TYPE_MAP.get(feature_class_name, None)
            if feature_class:
                geom = feature.geom
                geom.transform(ct)
                new_object = feature_class.create_or_update(feature, geom)
                new_object.sub_type = sub_type_name
                new_object.save()
            else:
                l_d("could not find feature class", feature_class_code, feature_class_name)


if __name__=='__main__':
    usage = "usage: %prog "
    parser = OptionParser(usage=usage,
        description="Load NOAA RNC catalog file into database, optionally slices tiles")
    parser.add_option("-d", "--debug", action="store_true", dest="debug")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet")
    parser.add_option("-f", "--directory", action="store", type="string", dest="directory")

    (options, args) = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG if options.debug else 
        (logging.ERROR if options.quiet else logging.INFO))
    l_d(options)
    print(options)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chartTracker.settings")
    from django.conf import settings

    import django
    django.setup()
    
    directory = options.directory
    if not directory:
        print "No directory specified(use -f), useing CWD"
        directory = os.getcwd()

    loadFiles(directory)


