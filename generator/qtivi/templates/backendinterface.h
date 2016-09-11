{% set class = 'QIvi{0}BackendInterface'.format(interface) %}

#pragma once

QT_BEGIN_NAMESPACE

class {{class}} : public QObject
{    
    explicit {{class}}(QObject *parent = Q_NULLPTR);

    virtual void initialize() = 0;

{% for property in interface.properties %}
    virtual void set{{property|upperfirst}}({{property|parameterType}}) = 0;
{% endfor %}

Q_SIGNALS
{% for property in interface.properties %}
    void {{property}}Changed({{property|parameterType}});
{% endfor %}
};

#define {{interface}}_iid "org.qt-project.qtivi.{{interface}}/1.0"

QT_END_NAMESPACE
