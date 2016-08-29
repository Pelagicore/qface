{% from 'helper.tpl' import module %}
#############################################################################
## This is an auto-generated file.
## Do not edit! All changes made to it will be lost.
#############################################################################

QT += qml quick
CONFIG += c++11


SOURCES += \
    {{module(package)|lower}}.cpp \
{% for service in package.services %}
    {{service|lower}}.cpp \
{% endfor %}
{% for struct in package.structs %}
    {{struct|lower}}.cpp \
{% endfor %}
    plugin.cpp

HEADERS += \
    {{module(package)|lower}}.h \
{% for service in package.services %}
    {{service|lower}}.h \
{% endfor %}
{% for struct in package.structs %}
    {{struct|lower}}.h \
{% endfor %}
    plugin.h
