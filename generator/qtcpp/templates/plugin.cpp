{# Copyright (c) Pelagicore AG 2016 #}
{% from 'helper.tpl' import module %}
{% set module = module(package) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "plugin.h"

#include <qqml.h>

#include "{{module|lower}}.h"

{% for service in package.services %}
#include "{{service|lower}}.h"
{% endfor %}

void Plugin::registerTypes(const char *uri)
{
    Qml{{module}}::registerTypes();    
    // @uri {{package|lower}}
    {% for service in package.services %}
    Qml{{module}}::registerQmlTypes(uri, 1, 0);    
    Qml{{service}}::registerQmlTypes(uri, 1, 0);
    {% endfor %}
}
