# Copyright (c) Pelagicore AB 2016
"""
A profile is a set of features describing a qface language profile.
The language profile tells the parser which language aspects are
supported for the particular choosen profile.

from profile import get_features, EProfile, EFeature

features = get_features(EProfile.ADVANCED)

if EFeature.CONST_OPERATION in features:
    # parse this aspect of the language

"""

from enum import Enum


class EFeature(Enum):
    CONST_OPERATION = 'const_operation'
    EXTEND_INTERFACE = 'extend_interface'
    IMPORT = 'import'
    MAPS = 'maps'


class EProfile(Enum):
    MICRO = 'micro'
    ADVANCED = 'advanced'
    FULL = 'full'


_profiles = {
    EProfile.MICRO: set(),
    EProfile.ADVANCED: set([
        EFeature.EXTEND_INTERFACE,
        EFeature.IMPORT,
        EFeature.MAPS
    ]),
    EProfile.FULL: set(EFeature)
}


def get_features(name):
    return _profiles.get(name, set())
