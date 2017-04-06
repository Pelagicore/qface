# Copyright (c) Pelagicore AB 2016

from enum import Enum


class EFeature(Enum):
    CONST_PROPERTY = 'const_property'
    EXTEND_INTERFACE = 'extend_interface'


class EProfile(Enum):
    BASIC = 'basic'
    ADVANCED = 'advanced'
    ALL = 'advanced'


class Profile:
    def __init__(self, features=set()):
        self.features = features

    @staticmethod
    def get_profile(cls, name):
        if name is EProfile.BASIC:
            return Profile(features=[
            ])
        if name is EProfile.ADVANCED:
            return Profile(features=[
                EFeature.CONST_PROPERTY,
                EFeature.EXTEND_INTERFACE
            ])
        if name is EProfile.ALL:
            return Profile(features=[
            ])
        return []


