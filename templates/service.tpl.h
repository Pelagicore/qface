# pragma once

#include <QtCore>

class {{service}} : public QObject
{
    Q_OBJECT
{% for attribute in service.attributes %}
    Q_PROPERTY({{attribute|returnType}} {{attribute}} READ {{attribute}} {%if not attribute.is_readonly%}WRITE set{{attribute|upperfirst}} {%endif%}NOTIFY {{attribute}}Changed)
{% endfor %}

public:
    {{service}}(QObject *parent=0);

public Q_SLOTS:
{% for operation in service.operations %}
    {{operation|returnType}} {{operation}}();
{% endfor %}

public:
{% for attribute in service.attributes %}
    void set{{attribute|upperfirst}}({{ attribute|parameterType }});
    {{attribute|returnType}} {{attribute}}() const;

{% endfor %}
Q_SIGNALS:
{% for attribute in service.attributes %}
    void {{attribute}}Changed({{attribute|parameterType}});
{% endfor %}

private:
{% for attribute in service.attributes %}
    {{attribute|returnType}} m_{{attribute}};
{% endfor %}
};
