/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "plugin.h"

#include <qqml.h>

{% for service in package.services %}
#include "{{service|lower}}.h"
{% endfor %}
{% for enum in package.enums %}
#include "{{enum|lower}}.h"
{% endfor %}
{% for struct in package.structs %}
#include "{{struct|lower}}.h"
#include "{{struct|lower}}factory.h"
{% endfor %}

{% for struct in package.structs %}
static QObject *{{struct|lower}}factory_qobject_singletontype_provider(QQmlEngine *engine, QJSEngine *scriptEngine)
{
  Q_UNUSED(engine)
  Q_UNUSED(scriptEngine)

  {{struct}}Factory *singleton = new {{struct}}Factory();
  return singleton;
}
{% endfor %}

void Plugin::registerTypes(const char *uri)
{
    // @uri {{package|lower}}
    {% for service in package.services %}
    qmlRegisterType<{{service}}>(uri, 1, 0, "{{service}}");
    {% endfor %}
    {% for enum in package.enums %}
    qmlRegisterUncreatableType<{{enum}}>(uri, 1, 0, "{{enum}}", "Enum type can not be created");
    {% endfor %}
    {% for struct in package.structs %}
    qRegisterMetaType<{{struct}}>();
    qmlRegisterSingletonType<{{struct}}Factory>(uri, 1, 0, "{{struct}}Factory", {{struct|lower}}factory_qobject_singletontype_provider);
    {% endfor %}
}
