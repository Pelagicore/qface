{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}'.format(struct) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#pragma once

#include <QtCore>

class {{class}}
{
    Q_GADGET
{% for field in struct.fields %}
    Q_PROPERTY({{field|returnType}} {{field}} MEMBER m_{{field}})
{% endfor %}

public:
{% for field in struct.fields %}
    {{field|returnType}} m_{{field}};
{% endfor %}

    bool operator==(const {{class}} &other) const;
};

Q_DECLARE_METATYPE({{class}})


