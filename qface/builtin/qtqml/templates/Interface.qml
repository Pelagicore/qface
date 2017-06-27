{% include 'copyright.h' %}


/*
 * This is a preserved file.
 * Changes will not be overriden by the generator.
 * To reset the file you need to delete it first.
 */

{% if 'singleton' in interface.tags %}
pragma Singleton
{% endif %}

import QtQml 2.2

import "private"

Abstract{{interface}} {
    id: root
}

