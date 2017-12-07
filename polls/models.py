from django.db import models

class ScriptModel(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='#')

    def __str__(self):
        return self.name

class PitchUpScraperModel(models.Model):
    name = models.CharField(max_length=100)

    ALL = 'All'
    CUSTOM = 'Custom'

    SCOTLAND = 'Scotland'
    NORTHERNIRELAND = 'Northern Ireland'
    REPUBLICOFIRELAND = 'Republic Of Ireland'
    WALES = 'Wales'
    ENGLAND = 'England'
    ENGLANDSOUTHWEST = 'England South West'
    ENGLANDSOUTHEAST = 'England South East'
    ENGLANDEASTANGLIA = 'England East Anglia'
    ENGLANDCENTRAL = 'England Central'
    ENGLANDNORTHWEST = 'England North West'
    ENGLANDNORTHEAST = 'England North East'

    REGIONS = (
        (ALL, 'All'),
        (SCOTLAND, 'Scotland'),
        (NORTHERNIRELAND, 'NorthernIreland'),
        (REPUBLICOFIRELAND, 'RepublicOfIreland'),
        (WALES, 'Wales'),
        (ENGLAND, 'England'),
        (ENGLANDSOUTHWEST, 'EnglandSouthWest'),
        (ENGLANDSOUTHEAST, 'EnglandSouthEast'),
        (ENGLANDEASTANGLIA, 'EnglandEastAnglia'),
        (ENGLANDCENTRAL, 'EnglandCentral'),
        (ENGLANDNORTHWEST, 'EnglandNorthWest'),
        (ENGLANDNORTHWEST, 'EnglandNorthEast'),
    )

    PAGES_COUNT = (
        (ALL, 'All'),
        (CUSTOM, 'Custom')
    )

