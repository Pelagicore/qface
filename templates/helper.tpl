{% macro module(package) -%}
{{package.nameParts|last|capitalize}}Module
{%- endmacro %}
