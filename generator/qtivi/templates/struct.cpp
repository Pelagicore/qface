{% set class = 'QIvi{0}'.format(struct) %}

#include "{{class|lower}}.h"

QT_BEGIN_NAMESPACE

class {{class}}Private : public QSharedDataPointer
{
public:
    {{class}}Private()
    : 
    {% for field in struct.fields %}
    , m_{{field}}(XXX)
    {% endfor %}
    {}

    {{class}}Private(const {{class}}Private &other)
    : QSharedData(other)
    {% for field in struct.fields %}
    , m_{{field}}(other.m_{{field}})
    {% endfor %}
    {}

    {% for field in struct.fields %}
    {{field|returnType}} m_{{field}};
    {% endfor %}
};

QT_END_NAMESPACE

{{class}}::{{class}}()
    : QIviSearchAndBrowseModelItem()
    , d(new {{class}}Private)
{    
}

{{class}}::{{class}}(const {{class}} &rhs)
    : QIviSearchAndBrowseModelItem(rhs)
    , d(rhs.d)
{    
}

{{class}} &{{class}}::operator=(const {{class}} &rhs)
{
    QIviSearchAndBrowseModelItem::operator=(rhs);
    if (this != &rhs)
        d.operator=(rhs.d);
    return *this;
}

{{class}}::~{{class}}()
{
}

{% for field in struct.fields %}
void {{class}}::set{{field|upperfirst}}({{ field|parameterType }})
{
    d->m_{{field}} = {{field}};
}

{{field|returnType}} {{class}}::{{field}}() const
{
    return d->m_{{field}};    
}
{% endfor %}

QString {{class}}::name() const
{
    return "XXX";
}

QString {{class}}::type() const
{
    return QLatin1String("{{struct|lower}}");
}

bool {{class}}::operator==(const {{class}} &other)
{
    return (QIviSearchAndBrowseModelItem::operator==(other)
            {% for field in struct.fields %}
            && d->m_{{field}} == other.d->m_{{member}}
            {%endfor%}
            );
}





