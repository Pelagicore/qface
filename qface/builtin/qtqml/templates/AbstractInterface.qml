import QtQml 2.2
import QtQml.Models 2.2

import "."

{{interface.comment}}
QtObject {
    id: root
    {% for property in interface.properties %}
    {{property.comment}}
    property {{property|propertyType}} {{property}} : {{property|defaultValue}}
    {% endfor %}

    {% for operation in interface.operations %}
    {{operation.comment}}
    property var {{operation}} : function({{operation.parameters|join(', ')}}) {}
    {% endfor %}

    {% for event in interface.events %}
    signal {{event}}(
        {%- for parameter in event.parameters %}
            {{- parameter.type|propertyType }} {{ parameter.name -}}
            {% if not loop.last %}, {% endif %}
        {% endfor -%}
    )
    {% endfor %}

}
