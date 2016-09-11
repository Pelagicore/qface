{% set class = 'QIvi{0}'.format(struct) %}

#include "{{class|lower}}.h"

QT_BEGIN_NAMESPACE

class {{class}}Private : public QSharedDataPointer
{
public:
    {{class}}Private()
    : 
    {% for member in struct.members %}
    , m_{{member}}(XXX)
    {% endfor %}
    {}

    {{class}}Private(const {{class}}Private &other)
    : QSharedData(other)
    {% for member in struct.members %}
    , m_{{member}}(other.m_{{member}})
    {% endfor %}
    {}

    {% for member in struct.members %}
    {{member|returnType}} m_{{member}};
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

{% for member in struct.members %}
void {{class}}::set{{member|upperfirst}}({{ member|parameterType }})
{
    d->m_{{member}} = {{member}};
}

{{member|returnType}} {{class}}::{{member}}() const
{
    return d->m_{{member}};    
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
            {% for member in struct.members %}
            && d->m_{{member}} == other.d->m_{{member}}
            {%endfor%}
            );
}





