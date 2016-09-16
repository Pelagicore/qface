{# Copyright (c) Pelagicore AB 2016 #}
{% macro qualifiedModuleName(module) -%}
{{module.nameParts|last|capitalize}}Module
{%- endmacro %}
