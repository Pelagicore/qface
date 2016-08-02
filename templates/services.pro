TEMPLATE = app

SOURCES += \
{% for service in package.services %}
    {{service|lower}}.cpp
{% endfor %}

HEADERS += \
{% for service in package.services %}
    {{service|lower}}.h
{% endfor %}
