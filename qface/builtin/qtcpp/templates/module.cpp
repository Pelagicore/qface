{# Copyright (c) Pelagicore AB 2016 #}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/
{% set class = 'Qml{0}Module'.format(module.module_name) %}


#include "{{class|lower}}.h"

#include <QtQml>

/*!
   \qmlmodule {{module}} 1.0
{% with doc = module.comment|parse_doc %}

   {{doc.brief}}


   {{doc.description}}
{% endwith %}
 */


/*!
   \qmltype {{module.module_name}}Module
   \inqmlmodule {{module}}
   \brief API to access module functionality

   Provides the enumerations and data type factories for
   this module.
*/
QObject* {{class|lower}}_singletontype_provider(QQmlEngine*, QJSEngine*)
{
    return new {{class}}();
}

{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{
}

{% for struct in module.structs %}
/*!
   \qmlmethod {{struct}} {{module.module_name}}Module::create{{struct}}()
   \brief Creates a default constructed data object from type {{struct}}
*/
Qml{{struct}} {{class}}::create{{struct}}()
{
    return Qml{{struct}}();
}
{% endfor %}

void {{class}}::registerTypes()
{
    {% for struct in module.structs %}
    qRegisterMetaType<Qml{{struct}}>();
    {% endfor %}
    {% for enum in module.enums %}
    qRegisterMetaType<{{class}}::{{enum}}>();
    {% endfor %}
}

void {{class}}::registerQmlTypes(const QString& uri, int majorVersion, int minorVersion)
{
    {% for struct in module.structs %}
    qmlRegisterUncreatableType<Qml{{struct}}Model>(uri.toLatin1(), majorVersion, minorVersion, "{{struct}}Model", "Model can not be instantiated from QML");
    {% endfor %}
    qmlRegisterSingletonType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{module.module_name}}Module", {{class|lower}}_singletontype_provider);
}


{% for enum in module.enums %}
/**
 * \qmlproperty enumeration {{module.module_name}}Module::{{enum}}
 * \list
 {% for member in enum.members %}
 * \li {{member}}
 {% endfor %}
 * \endlist
 */
{% endfor %}