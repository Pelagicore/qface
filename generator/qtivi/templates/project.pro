TARGET = QtIvi{{module|upperfirst}}

QT = core-private ivicore ivicore-private
CONFIG += c++11
VERSION = 1.0.0

OTHER_FILES += \
    $$PWD/doc/*.qdocconf \
    $$PWD/doc/src/*.qdoc

CMAKE_MODULE_TESTS = '-'

HEADERS += \
{% for interface in module.interfaces %}
    {{interface|className|lower}}.h \
    {{interface|className|lower}}_p.h \
    {{interface|className|lower}}backendinterface.h \
{% endfor %}

SOURCES += \
{% for interface in module.interfaces %}
    {{interface|className|lower}}.cpp \
    {{interface|className|lower}}backendinterface.cpp \
{% endfor %}

load(qt_module)
