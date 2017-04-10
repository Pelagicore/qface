import QtQml 2.2
import QtQml.Models 2.2

import "."

{{interface.comment}}
QtObject {
    id: root
{% for property in interface.properties %}
    {{property.comment}}
{% if property.readonly %}
    readonly property {{property|propertyType}} {{property}} : _{{property}}
    property {{property|propertyType}} _{{property}} : {{property|defaultValue}}
{% else %}
    property {{property|propertyType}} {{property}} : {{property|defaultValue}}
{% endif %}
{% endfor %}
{% for operation in interface.operations %}
    {{operation.comment}}
    property var {{operation}} : function({{operation.parameters|join(', ')}}) {}
{% endfor %}

{% for signal in interface.signals %}
    signal {{signal}}(
        {%- for parameter in signal.parameters %}
            {{- parameter.type|propertyType }} {{ parameter.name -}}
            {% if not loop.last %}, {% endif %}
        {% endfor -%}
    )
{% endfor %}

}
