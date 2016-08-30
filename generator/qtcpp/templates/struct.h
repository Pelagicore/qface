{# Copyright (c) Pelagicore AG 2016 #}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#pragma once

#include <QtCore>

class {{struct}}
{
    Q_GADGET
{% for member in struct.members %}
    Q_PROPERTY({{member|returnType}} {{member}} MEMBER m_{{member}})
{% endfor %}

public:
{% for member in struct.members %}
    {{member|returnType}} m_{{member}};
{% endfor %}

    bool operator==(const {{struct}} &other) const;
};

Q_DECLARE_METATYPE({{struct}})


