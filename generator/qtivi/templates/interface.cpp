{% set class = 'QIvi{0}'.format(interface) %}

#include "{{class|lower}}.h"
#include "{{class|lower}}_p.h"

{{class}}Private::{{class}}Private(const QString &interface, {{class}} *parent)
    : QIviAbstractFeaturePrivate(interface, parent)
    , q_ptr(parent)
{% for property in interface.properties %}
    , m_{{property}}(XXX)
{% endfor %}
{
}

void {{class}}Private::clearToDefaults()
{    
{% for property in interface.properties %}
    m_{{property}} = XXX;
{% endfor %}
}

{% for property in interface.properties %}
void {{class}}Private::on{{property|upperfirst}}Changed({{property|parameterType}})
{
    if (m_{{property}} == {{property}})
        return;
    Q_Q({{class}});
    m_{{property}} = {{property}};
    emit q->{{property}}Changed({{property}});
}
{% endfor %}


{{class}}::{{class}}(QObject *parent)
    : QIviAbstractFeature(*new {{class}}Private(QLatin1String({{class}}_iid), this), parent)
{
}

{% for property in interface.properties %}
{{property|returnType}} {{class}}::{{property}}() const
{
    Q_D(const {{class}});
    return d->m_{{property}};
}

void {{class}}::set{{property|upperfirst}}({{property|parameterType}})
{    
    Q_D(const {{class}});
    {{class}}BackendInterface *backend = d->{{interface|lower}}Backend();
    if (!backend) {
        qWarning("Can not set {{property}} without a connected backend");
        return;
    }
    backend->set{{property|upperfirst}}({{property}});
}
{% endfor %}

{% for operation in interface.operations %}
{{operation|returnType}} {{class}}::{{operation}}(XXX)
{
    Q_D(const {{class}});
    {{class}}BackendInterface *backend = d->{{interface|lower}}Backend();
    if (!backend) {
        qWarning("Can not {{operation}} without a connected backend");
        return;
    }
    backend->{{operation}}(XXX);
}
{% endfor %}


{{class}}::{{class}}({{class}}Private &dd, QObject *parent)
    : QIviAbstractFeature(dd, parent)
{
}

bool {{class}}::acceptServiceObject(QIviServiceObject *serviceObject)
{
    return serviceObject->interfaces().contains(QLatin1String({{class}}_iid));
}

void {{class}}::connectToServiceObject(QIviServiceObject *serviceObject)
{    
    Q_UNUSED(serviceObject);

    Q_D({{class}});

    {{class}}BackendInterface *backend = d->{{interface|lower}}Backend();
    if (!backend)
        return;
{% for property in interface.properties %}
    QObjectPrivate::connect(backend, &{{class}}BackendInterface::{{property}}Changed,
                            d, &{{class}}Private::on{{property|upperfirst}}Changed);
{% endfor %}
    backend->initialize();
}

void {{class}}::disconnectFromServiceObject(QIviServiceObject *serviceObject)
{
    {{class}}BackendInterface *backend = qobject_cast<{{class}}BackendInterface*>(serviceObject->interfaceInstance(QLatin1String({{class}}_iid)));

    if (backend)
        disconnect(backend, 0, this, 0);
}

void {{class}}::clearServiceObject()
{  
    Q_D({{class}});
    d->clearToDefaults();
}







