{% set class = 'QIvi{0}'.format(struct) %}

#pragma once

QT_BEGIN_NAMESPACE

class {{class}}Private;

class {{class}} : public QIviSearchAndBrowseModelItem
{
    Q_GADGET
{% for field in struct.fields %}
    Q_PROPERTY({{field|returnType}} {{field}} READ {{field}} WRITE set{{field|upperfirst}})
{% endfor %}
public:
    {{class}}();
    {{class}}(const {{class}} &);
    {{class}} &operator=(const {{class}} &);
    virtual ~{{class}}();

{% for field in struct.fields %}
    void set{{field|upperfirst}}({{ field|parameterType }});
    {{field|returnType}} {{field}}() const;
{% endfor %}

    virtual QString name() const Q_DECL_OVERRIDE;
    virtual QString type() const Q_DECL_OVERRIDE;

    bool operator==(const {{class}} &other);
    inline bool operator!=(const {{class}} &other) { return !(*this == other); }
private:
    QSharedDataPointer<{{class}}Private> d;
};

Q_DECLARE_TYPEINFO({{class}}, Q_MOVABLE_TYPE);

QT_END_NAMESPACE

Q_DECLARE_METATYPE({{class}})
