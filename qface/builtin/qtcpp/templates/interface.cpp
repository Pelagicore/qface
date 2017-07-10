{# Copyright (c) Pelagicore AB 2016 #}
{% import "qtcpp.j2" as cpp %}
{{ cpp.preserved() }}
{% set class = '{0}'.format(interface) %}

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
    : Abstract{{interface}}(parent)
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
