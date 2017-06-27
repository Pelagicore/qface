{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}'.format(interface) %}
/*
 * This is a preserved file.
 * Changes will not be overriden by the generator.
 * To reset the file you need to delete it first.
 */

#include "{{class|lower}}.h"

#include <QtQml>


/*!
    \inqmlmodule {{module}} 1.0
 */

QObject* {{class|lower}}_singletontype_provider(QQmlEngine*, QJSEngine*)
{
      return new {{class}}();
}


/*!
   \qmltype {{interface}}
   \inqmlmodule {{module}}
{% with doc = interface.comment|parse_doc %}
   \brief {{doc.brief}}

   {{doc.description}}
{% endwith %}
*/

{{interface.comment}}
{{class}}::{{class}}(QObject *parent)
    : QmlAbstract{{interface}}(parent)
{
}

{{class}}::~{{class}}()
{
}

void {{class}}::registerQmlTypes(const QString& uri, int majorVersion, int minorVersion)
{
    {% if 'singleton' in interface.tags %}
    qmlRegisterSingletonType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{interface}}", {{class|lower}}_singletontype_provider);
    {% else %}
    qmlRegisterType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{interface}}");
    {% endif %}
}
