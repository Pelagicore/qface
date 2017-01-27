import QtQml 2.2
import QtQml.Models 2.2

import "."

QtObject {
    {% for property in interface.properties %}
    property {{property|propertyType}} {{property}} : {{property|defaultValue}}
    {% endfor %}

    {% for operation in interface.operations %}
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
