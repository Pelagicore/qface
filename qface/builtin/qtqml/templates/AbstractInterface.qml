{% include 'copyright.h' %}


/*
 * This is an auto-generated file.
 * Do not edit! All changes made to it will be lost.
 */

import QtQml 2.2
import QtQml.Models 2.2

import "."

{{interface.comment}}
QtObject {
    id: root

{% for property in interface.properties %}
{% if property.readonly %}
{% if property.comment %}
    {{ property.comment }}
{% endif %}
    readonly property {{property|propertyType}} {{property}} : _{{property}}
    property {{property|propertyType}} _{{property}} : {{property|defaultValue}}
{% else %}
{% if property.comment %}
    {{ property.comment }}
{% endif %}
    property {{property|propertyType}} {{property}} : {{property|defaultValue }}
{% endif %}
{% endfor %}

{% for operation in interface.operations %}
{% if operation.comment %}
    {{ operation.comment }}
{% endif %}
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

