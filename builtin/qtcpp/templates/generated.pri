{# Copyright (c) Pelagicore AB 2016 #}
#############################################################################
## This is an auto-generated file.
## Do not edit! All changes made to it will be lost.
#############################################################################

QT += qml quick
CONFIG += c++11

HEADERS += \
    $$PWD/qml{{module.module_name|lower}}module.h \
{% for interface in module.interfaces %}
    $$PWD/qmlabstract{{interface|lower}}.h \
{% endfor %}
{% for struct in module.structs %}
    $$PWD/qml{{struct|lower}}.h \
    $$PWD/qml{{struct|lower}}model.h {% if not loop.last %}\{% endif %}
{% endfor %}
    

SOURCES += \
    $$PWD/qml{{module.module_name|lower}}module.cpp \
{% for interface in module.interfaces %}
    $$PWD/qmlabstract{{interface|lower}}.cpp \
{% endfor %}
{% for struct in module.structs %}
    $$PWD/qml{{struct|lower}}.cpp \
    $$PWD/qml{{struct|lower}}model.cpp {% if not loop.last %}\{% endif %}
{% endfor %}


