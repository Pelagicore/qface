import QtQml 2.2
import QtQml.Models 2.2

import "."

{{interface.comment}}
QtObject {
    id: root
    {% for property in interface.properties %}
    {{property.comment}}
    readonly property {{property|propertyType}} {{property}} : _provider.{{property}}
    {% endfor %}

    {% for operation in interface.operations %}
    {{operation.comment}}
    readonly property var {{operation}} : _provider.{{operation}}
    {% endfor %}

    property {{interface}}Provider _provider: {{interface}}Provider {}
}
