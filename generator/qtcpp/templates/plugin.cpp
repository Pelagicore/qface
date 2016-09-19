{# Copyright (c) Pelagicore AB 2016 #}
{% from 'helper.tpl' import qualifiedModuleName %}
{% set moduleName = qualifiedModuleName(module) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "plugin.h"

#include <qqml.h>

#include "qml{{moduleName|lower}}.h"

{% for interface in module.interfaces %}
#include "{{interface|lower}}.h"
{% endfor %}

void Plugin::registerTypes(const char *uri)
{
    Qml{{moduleName}}::registerTypes();    
    // @uri {{module|lower}}
    Qml{{moduleName}}::registerQmlTypes(uri, 1, 0);
{% for interface in module.interfaces %}
    Qml{{interface}}::registerQmlTypes(uri, 1, 0);
{% endfor %}
}
