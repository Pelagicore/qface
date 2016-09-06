{# Copyright (c) Pelagicore AG 2016 #}
{% from 'helper.tpl' import qualifiedModuleName %}
{% set moduleName= qualifiedModuleName(module) %}
{% set class = 'Qml{0}'.format(interface) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#pragma once

#include <QtCore>

#include "{{moduleName|lower}}.h"

class {{class}} : public QObject
{
    Q_OBJECT
{% for attribute in interface.attributes %}
    Q_PROPERTY({{attribute|returnType}} {{attribute}} READ {{attribute}} {%if not attribute.is_readonly%}WRITE set{{attribute|upperfirst}} {%endif%}NOTIFY {{attribute}}Changed)
{% endfor %}

public:
    {{class}}(QObject *parent=0);

    static void registerQmlTypes(const QString& uri, int majorVersion=1, int minorVersion=0);

public Q_SLOTS:
{% for operation in interface.operations %}
    {{operation|returnType}} {{operation}}();
{% endfor %}

public:
{% for attribute in interface.attributes %}
    void set{{attribute|upperfirst}}({{ attribute|parameterType }});
    {{attribute|returnType}} {{attribute}}() const;

{% endfor %}
Q_SIGNALS:
{% for attribute in interface.attributes %}
    void {{attribute}}Changed({{attribute|parameterType}});
{% endfor %}

private:
{% for attribute in interface.attributes %}
    {{attribute|returnType}} m_{{attribute}};
{% endfor %}
};
