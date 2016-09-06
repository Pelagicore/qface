{# Copyright (c) Pelagicore AG 2016 #}
{% from 'helper.tpl' import qualifiedModuleName %}
{% set moduleName = qualifiedModuleName(module) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "plugin.h"

#include <qqml.h>

#include "{{moduleName|lower}}.h"

{% for interface in module.interfaces %}
#include "{{interface|lower}}.h"
{% endfor %}

void Plugin::registerTypes(const char *uri)
{
    Qml{{module}}::registerTypes();    
    // @uri {{module|lower}}
    {% for interface in module.interfaces %}
    Qml{{moduleName}}::registerQmlTypes(uri, 1, 0);
    Qml{{interface}}::registerQmlTypes(uri, 1, 0);
    {% endfor %}
}
