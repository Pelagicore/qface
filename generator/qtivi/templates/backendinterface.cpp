{% set class = 'QIvi{0}BackendInterface'.format(interface) %}

#include "{{class|lower}}.h"

{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{
}
