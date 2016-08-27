TEMPLATE = lib
QT += qml quick
CONFIG += qt plugin c++11
TARGET = $$qtLibraryTarget({{package|lower}})

uri = {{package}}

include( {{package|lower}}.pri )
