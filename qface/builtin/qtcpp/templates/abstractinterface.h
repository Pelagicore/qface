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
    Q_PROPERTY({{property|returnType}} {{property}} READ {{property}} {% if not property.is_readonly %}WRITE set{{property|upperfirst}} {% endif %}{% if not property.is_const %}NOTIFY {{property}}Changed{% endif %})
{% endfor %}

public:
    {{class}}(QObject *parent = nullptr);
    ~{{class}}();

public Q_SLOTS:
{% for operation in interface.operations %}
    virtual {{operation|returnType}} {{operation}}({{operation.parameters|map('parameterType')|join(', ')}});
{% endfor %}

public:
{% for property in interface.properties %}
    virtual void set{{property|upperfirst}}({{ property|parameterType }});
{% endfor %}

public:
{% for property in interface.properties %}
    virtual {{property|returnType}} {{property}}() const;
{% endfor %}

Q_SIGNALS:
{% for signal in interface.signals %}
    void {{signal}}({{signal.parameters|map('parameterType')|join(', ')}});
{% endfor %}
{% for property in interface.properties %}
    void {{property}}Changed();
{% endfor %}

protected:
{% for property in interface.properties %}
    {{property|returnType}} m_{{property}};
{% endfor %}
};
