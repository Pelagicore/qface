{# Copyright (c) Pelagicore AB 2016 #}
{% import "qtcpp.j2" as cpp %}
{{ cpp.preserved(prefix="##")}}

TEMPLATE = lib
QT += qml quick
CONFIG += qt plugin c++11
TARGET = $$qtLibraryTarget({{module|lower}})

uri = {{module}}


HEADERS += \
{% for interface in module.interfaces %}
    qml{{interface|lower}}.h \
{% endfor %}
    plugin.h


SOURCES += \
{% for interface in module.interfaces %}
    qml{{interface|lower}}.cpp \
{% endfor %}
    plugin.cpp


include( generated/generated.pri )
include( docs/docs.pri )

DISTFILES = qmldir

!equals(_PRO_FILE_PWD_, $$OUT_PWD) {
    copy_qmldir.target = $$OUT_PWD/qmldir
    copy_qmldir.depends = $$_PRO_FILE_PWD_/qmldir
    copy_qmldir.commands = $(COPY_FILE) \"$$replace(copy_qmldir.depends, /, $$QMAKE_DIR_SEP)\" \"$$replace(copy_qmldir.target, /, $$QMAKE_DIR_SEP)\"
    QMAKE_EXTRA_TARGETS += copy_qmldir
    PRE_TARGETDEPS += $$copy_qmldir.target
}

qmldir.files = qmldir
unix {
    installPath = $$[QT_INSTALL_QML]/$$replace(uri, \\., /)
    qmldir.path = $$installPath
    target.path = $$installPath
    INSTALLS += target qmldir
}
