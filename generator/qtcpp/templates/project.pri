{# Copyright (c) Pelagicore AG 2016 #}
{% from 'helper.tpl' import module %}
#############################################################################
## This is an auto-generated file.
## Do not edit! All changes made to it will be lost.
#############################################################################

QT += qml quick
CONFIG += c++11


HEADERS += \
    {{qualifiedModuleName(module)|lower}}.h \
{% for interface in module.interfaces %}
    {{interface|lower}}.h \
{% endfor %}
{% for struct in module.structs %}
    {{struct|lower}}.h \
    {{struct|lower}}model.h \
{% endfor %}
    plugin.h

SOURCES += \
    {{qualifiedModuleName(module)|lower}}.cpp \
{% for interface in module.interfaces %}
    {{interface|lower}}.cpp \
{% endfor %}
{% for struct in module.structs %}
    {{struct|lower}}.cpp \
    {{struct|lower}}model.cpp \
{% endfor %}
    plugin.cpp
