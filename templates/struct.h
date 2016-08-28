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
    Q_PROPERTY({{member|returnType}} {{member}} READ {{member}} WRITE set{{member|upperfirst}})
{% endfor %}

public:
    {{struct}}();
    ~{{struct}}();
public:
{% for member in struct.members %}
    void set{{member|upperfirst}}({{ member|parameterType }});
    {{member|returnType}} {{member}}() const;
{% endfor %}

private:
{% for member in struct.members %}
    {{member|returnType}} m_{{member}};
{% endfor %}
};

Q_DECLARE_METATYPE({{struct}})


