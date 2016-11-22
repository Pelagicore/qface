{# Copyright (c) Pelagicore AB 2016 #}
{% set module_name = 'Qml{0}Module'.format(module.module_name()) %}
#############################################################################
## This is an auto-generated file.
## Do not edit! All changes made to it will be lost.
#############################################################################

QT += qml quick
CONFIG += c++11


HEADERS += \
    {{module_name|lower}}.h \
{% for interface in module.interfaces %}
    {{interface|lower}}.h \
{% endfor %}
{% for struct in module.structs %}
    {{struct|lower}}.h \
    {{struct|lower}}model.h \
{% endfor %}
    plugin.h

SOURCES += \
    {{module_name|lower}}.cpp \
{% for interface in module.interfaces %}
    {{interface|lower}}.cpp \
{% endfor %}
{% for struct in module.structs %}
    {{struct|lower}}.cpp \
    {{struct|lower}}model.cpp \
{% endfor %}
    plugin.cpp
