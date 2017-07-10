{# Copyright (c) Pelagicore AB 2016 #}
{% import "qtcpp.j2" as cpp %}
{% set class = 'QmlAbstract{0}'.format(interface) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "{{class|lower}}.h"

#include <QtQml>


/*!
   \qmltype {{interface}}
   \inqmlmodule {{module}}
{% with doc = interface.comment|parse_doc %}
   \brief {{doc.brief}}

   {{doc.description}}
{% endwith %}
*/
{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{% for property in interface.properties %}
    , m_{{property}}({{property|defaultValue}})
{% endfor %}
{
}


{{class}}::~{{class}}()
{
}

{% for property in interface.properties %}
{{ cpp.property_setter_impl(class, property) }}

{{ cpp.property_getter_impl(class, property) }}
{% endfor %}

{%- for operation in interface.operations %}
{{ cpp.operation_impl(class, operation) }}
{% endfor %}


