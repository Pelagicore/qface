{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}Model'.format(struct) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "{{class|lower}}.h"

{{class}}::{{class}}(QObject *parent)
    : QAbstractListModel(parent)
{
    {% for field in struct.fields %}
    m_roleNames.insert(Roles::{{field|upperfirst}}, QByteArray("{{field}}"));
    {% endfor %}
}

int {{class}}::count() const
{
    return m_data.count();
}

Qml{{struct}} {{class}}::get(int index)
{
    return m_data.value(index);
}

int {{class}}::rowCount(const QModelIndex &parent) const
{
    Q_UNUSED(parent)
    return m_data.count();
}

QVariant {{class}}::data(const QModelIndex &index, int role) const
{
    if(index.row() < 0 || index.row() >= count()) {
        return QVariant();
    }
    const Qml{{struct}} &{{struct|lower}} = m_data.at(index.row());
    switch(role) {
    {% for field in struct.fields %}
    case Roles::{{field|upperfirst}}:
        return QVariant::fromValue({{struct|lower}}.m_{{field}});
        break;
    {% endfor %}
    }
    return QVariant();
}

QHash<int, QByteArray> {{class}}::roleNames() const
{
    return m_roleNames;
}


void {{class}}::insert{{struct}}(int row, const Qml{{struct}} &{{struct|lower}})
{
    if (row < 0)
        row = 0;
    if (row >= m_data.count())
        row = m_data.count();
    
    beginInsertRows(QModelIndex(), row, row);
    m_data.insert(row, {{struct|lower}});
    endInsertRows();
    emit countChanged(count());
}

void {{class}}::update{{struct}}(int row, const Qml{{struct}} &{{struct|lower}})
{    
    if(row < 0 || row >= m_data.count()) {
        return;
    }
    m_data[row] = {{struct|lower}};
    const QModelIndex &index = createIndex(row, 0);
    emit dataChanged(index, index);
}

void {{class}}::remove{{struct}}(int row)
{
    if(row < 0 || row >= m_data.count()) {
        return;
    }
    beginRemoveRows(QModelIndex(), row, row);
    m_data.removeAt(row);
    endRemoveRows();
}

