{# Copyright (c) Pelagicore AB 2016 #}
{% set module_name = 'Qml{0}Module'.format(module.module_name) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "plugin.h"

#include <qqml.h>

#include "{{module_name|lower}}.h"

{% for interface in module.interfaces %}
#include "qmlabstract{{interface|lower}}.h"
{% endfor %}

void Plugin::registerTypes(const char *uri)
{
    {{module_name}}::registerTypes();    
    // @uri {{module|lower}}
    {{module_name}}::registerQmlTypes(uri, 1, 0);
{% for interface in module.interfaces %}
    QmlAbstract{{interface}}::registerQmlTypes(uri, 1, 0);
{% endfor %}
}
