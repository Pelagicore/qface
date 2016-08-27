QT += qml quick
CONFIG += c++11


SOURCES += \
    plugin.cpp \
{% for service in package.services %}
    {{service|lower}}.cpp
{% endfor %}

HEADERS += \
    plugin.h \
{% for service in package.services %}
    {{service|lower}}.h
{% endfor %}
