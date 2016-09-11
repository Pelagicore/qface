{% set class = 'QIvi{0}'.format(interface) %}
#pragma once

#include "private/qiviabstractfeature_p.h"

#include "{{class|lower}}.h"
#include "{{class|lower}}backendinterface.h"

QT_BEGIN_NAMESPACE

class {{class}}Private : public QIviAbstractFeaturePrivate
{
public:
    {{class}}Private(const QString &interface, {{class}} *parent);

    void clearToDefaults();

{% for property in interface.properties %}
    void on{{property|upperfirst}}Changed({{property|parameterType}})
{% endfor %}
    {{class}}BackendInterface *{{interface|lower}}Backend() const;

    {{class}} * const q_ptr;

{% for property in interface.properties %}
    {{property|returnType}} m_{{property}};
{% endfor %}

    Q_DECLARE_PUBLIC({{class}})
};

QT_END_NAMESPACE

