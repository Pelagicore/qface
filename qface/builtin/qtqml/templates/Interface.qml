{% if 'singleton' in interface.tags %}
pragma Singleton
{% endif %}

import QtQml 2.2

import "private"

Abstract{{interface}} {
    id: root
}
