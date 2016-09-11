{% set class = 'QIvi{0}'.format(interface) %}
#pragma once

#include <QtIviCore/QIviAbstractFeature>
#include <QtIvi{{module|upperfirst}}/qtivi{{module}}global.h>
#include <QtCore/QVariant>

QT_BEGIN_NAMESPACE

class Q_QTIVI{{module|upper}}_EXPORT {{class}}
{
    Q_OBJECT
{% for property in interface.properties %}
    Q_PROPERTY({{property|returnType}} {{property}} READ {{property}} {%if not property.is_readonly%}WRITE set{{property|upperfirst}} {%endif%}NOTIFY {{property}}Changed)
{% endfor %}
public:
    explicit {{class}}(QObject *parent=Q_NULLPTR);

{% for operation in interface.operations %}
    Q_INVOKABLE {{operation|returnType}} {{operation}}();    
{% endfor %}

{% for property in interface.properties %}
    void set{{property|upperfirst}}({{ property|parameterType }});
    {{property|returnType}} {{property}}() const;

{% endfor %}
Q_SIGNALS:
{% for property in interface.properties %}
    void {{property}}Changed({{property|parameterType}});
{% endfor %}
protected:
    {{class}}({{class}}Private &dd, QObject *parent = Q_NULLPTR);

    virtual bool acceptServiceObject(QIviServiceObject *serviceObject) Q_DECL_OVERRIDE;
    virtual void connectToServiceObject(QIviServiceObject *serviceObject) Q_DECL_OVERRIDE;
    virtual void disconnectFromServiceObject(QIviServiceObject *serviceObject) Q_DECL_OVERRIDE;
    virtual void clearServiceObject() Q_DECL_OVERRIDE;
private:
    Q_DECLARE_PRIVATE(QIviAmFmTuner)
{% for property in interface.properties %}
    Q_PRIVATE_SLOT(d_func(), void on{{property|upperfirst}}Changed({{property|parameterType}}))
{% endfor %}
};


QT_END_NAMESPACE

