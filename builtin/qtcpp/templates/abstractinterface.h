{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'QmlAbstract{0}'.format(interface) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#pragma once

#include <QtCore>

#include "qml{{module.module_name|lower}}module.h"

class {{class}} : public QObject
{
    Q_OBJECT
{% for property in interface.properties %}
    Q_PROPERTY({{property|returnType}} {{property}} READ {{property}} NOTIFY {{property}}Changed)
{% endfor %}

public:
    {{class}}(QObject *parent=0);
    ~{{class}}();

public Q_SLOTS:
{% for operation in interface.operations %}
    virtual {{operation|returnType}} {{operation}}({{operation.parameters|map('parameterType')|join(', ')}});
{% endfor %}

public:
{% for property in interface.properties %}
{% if not property.is_readonly %}
    virtual void set{{property|upperfirst}}({{ property|parameterType }});
{% endif %}
{% endfor %}

public:
{% for property in interface.properties %}
    virtual {{property|returnType}} {{property}}() const;
{% endfor %}

Q_SIGNALS:
{% for property in interface.properties %}
    void {{property}}Changed();
{% endfor %}

protected:
{% for property in interface.properties %}
    {{property|returnType}} m_{{property}};
{% endfor %}
};
