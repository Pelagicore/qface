{# Copyright (c) Pelagicore AB 2016 #}
{% from 'helper.tpl' import qualifiedModuleName %}
{% set moduleName = qualifiedModuleName(module) %}
#############################################################################
## This is an auto-generated file.
## Do not edit! All changes made to it will be lost.
#############################################################################

QT += qml quick
CONFIG += c++11


HEADERS += \
    qml{{moduleName|lower}}.h \
{% for interface in module.interfaces %}
    abstract{{interface|lower}}.h \
{% endfor %}
{% for struct in module.structs %}
    {{struct|lower}}.h \
    {{struct|lower}}model.h \
{% endfor %}
    plugin.h

SOURCES += \
    qml{{moduleName|lower}}.cpp \
{% for interface in module.interfaces %}
    abstract{{interface|lower}}.cpp \
{% endfor %}
{% for struct in module.structs %}
    {{struct|lower}}.cpp \
    {{struct|lower}}model.cpp \
{% endfor %}
    plugin.cpp
