{% include 'copyright.h' %}


/*
 * This is an auto-generated file.
 * Do not edit! All changes made to it will be lost.
 */

.pragma library

{% for enum in module.enums %}
// Enum: {{enum}}
{% for member in enum.members %}
var {{member}} = {{member.value}};
{% endfor %}
{% endfor %}

{% for struct in module.structs %}
function create{{struct}}() {
    return {
        {% for field in struct.fields %}
        {{field}} : {{field | defaultValue}},
        {% endfor %}
    };
}
{% endfor %}
