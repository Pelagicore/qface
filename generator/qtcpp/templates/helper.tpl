{# Copyright (c) Pelagicore AG 2016 #}
{% macro module(package) -%}
{{package.nameParts|last|capitalize}}Module
{%- endmacro %}
