
#include "plugin.h"

#include <qqml.h>

{% for service in package.services %}
#include "{{service|lower}}.h"
{% endfor %}

void Plugin::registerTypes(const char *uri)
{
    // @uri {{package|lower}}
    {% for service in package.services %}
    qmlRegisterType<{{service}}>(uri, 1, 0, "{{service}}");
    {% endfor %}
}
