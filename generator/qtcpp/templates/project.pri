{# Copyright (c) Pelagicore AG 2016 #}
{% from 'helper.tpl' import module %}
#############################################################################
## This is an auto-generated file.
## Do not edit! All changes made to it will be lost.
#############################################################################

QT += qml quick
CONFIG += c++11


HEADERS += \
    {{module(package)|lower}}.h \
{% for interface in package.interfaces %}
    {{interface|lower}}.h \
{% endfor %}
{% for struct in package.structs %}
    {{struct|lower}}.h \
    {{struct|lower}}model.h \
{% endfor %}
    plugin.h

SOURCES += \
    {{module(package)|lower}}.cpp \
{% for interface in package.interfaces %}
    {{interface|lower}}.cpp \
{% endfor %}
{% for struct in package.structs %}
    {{struct|lower}}.cpp \
    {{struct|lower}}model.cpp \
{% endfor %}
    plugin.cpp
