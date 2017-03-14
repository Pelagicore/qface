{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}'.format(struct) %}
{% set ampersand = joiner(" &&") %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "{{class|lower}}.h"



// Shared Data

class {{class}}Data : public QSharedData
{
public:
    {{class}}Data()
        : QSharedData()
    {% for field in struct.fields %}
        , {{field}}({{field|defaultValue}})
    {% endfor %}
    {
    }
    {{class}}Data(const {{class}}Data &other)
        : QSharedData(other)
    {% for field in struct.fields %}
        , {{field}}(other.{{field}})
    {% endfor %}
    {
    }

public:
{% for field in struct.fields %}
    {{field|returnType}} {{field}};
{% endfor %}
};

// Class

/*!
   \qmltype {{struct}}
   \inqmlmodule {{module}}
{% with doc = struct.comment|parse_doc %}
   \brief {{doc.brief}}

   {{doc.description}}
{% endwith %}
*/

{{class}}::{{class}}()
    : d(new {{class}}Data)
{
}

{{class}}::{{class}}(const {{class}} &other)
    : d(other.d)
{
}

{{class}}::~{{class}}()
{
}

{% for field in struct.fields %}
void {{class}}::set{{field|upperfirst}}({{field|parameterType}})
{
    d->{{field}} = {{field}};
}
{{field|returnType}} {{class}}::{{field}}() const
{
    return d->{{field}};
}

{% endfor %}



{{class}} {{class}}::clone()
{
    {{class}} other(*this);
    other.d.detach();
    return other;
}

bool {{class}}::operator==(const {{class}} &other) const
{
    return (
        {%- for field in struct.fields %}{{ ampersand() }}
        {{field}}() == other.{{field}}()
        {%- endfor %}
    );
}

{{class}} &{{class}}::operator=(const {{class}} &other)
{
    d = other.d;
    return *this;
}

