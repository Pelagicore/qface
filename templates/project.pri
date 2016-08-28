#############################################################################
## This is an auto-generated file.
## Do not edit! All changes made to it will be lost.
#############################################################################

QT += qml quick
CONFIG += c++11


SOURCES += \
{% for service in package.services %}
    {{service|lower}}.cpp \
{% endfor %}
{% for enum in package.enums %}
    {{enum|lower}}.cpp \
{% endfor %}
{% for struct in package.structs %}
    {{struct|lower}}.cpp \
    {{struct|lower}}factory.cpp \
{% endfor %}
    plugin.cpp

HEADERS += \
{% for service in package.services %}
    {{service|lower}}.h \
{% endfor %}
{% for enum in package.enums %}
    {{enum|lower}}.h \
{% endfor %}
{% for struct in package.structs %}
    {{struct|lower}}.h \
    {{struct|lower}}factory.h \
{% endfor %}
    plugin.h
