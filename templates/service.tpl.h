# pragma once

#include <QtCore>

class {{service}} : public QObject
{
    Q_OBJECT
{% for attribute in service.attributes %}
    Q_PROPERTY({{attribute}} READ {{attribute}} NOTIFY {{attribute}}Changed)
{% endfor %}
public:
    {{service}}(QObject *parent=0);
{% for operation in service.operations %}
    Q_INVOKABLE {{operation|returnType}} {{operation}}();
{% endfor %}
{% for attribute in service.attributes %}
    void set{{attribute|upperfirst}}({{ attribute|parameterType }});
    {{attribute|returnType}} {{attribute}}() const;

{% endfor %}
Q_SIGNALS:
{% for attribute in service.attributes %}
    void {{attribute}}Changed({{attribute|parameterType}})
{% endfor %}
private:
{% for attribute in service.attributes %}
    m_{{attribute}};
{% endfor %}
};
