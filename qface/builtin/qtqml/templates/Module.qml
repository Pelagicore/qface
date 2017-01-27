pragma Singleton

import QtQml 2.2

/**
 * {{module.comment}}
 */
QtObject {
    id: root

    {% for enum in module.enums %}
    // Enum: {{enum}}
    {% for member in enum.members %}
    readonly property int {{member}}: {{member.value}}
    {% endfor %}

    {% endfor %}

    {% for struct in module.structs %}
    function create{{struct}}() {
        return {};
    }
    {% endfor %}
}
