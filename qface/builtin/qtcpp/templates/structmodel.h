{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}Model'.format(struct) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#pragma once

#include <QtCore>

#include "qml{{struct|lower}}.h"

class {{class}} : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(int count READ count NOTIFY countChanged)
public:
    enum Roles { {{struct.fields|map('upperfirst')|join(', ')}} };
    {{class}}(QObject *parent = nullptr);
    Q_INVOKABLE Qml{{struct}} get(int index);
    int count() const;
    void insert(int row, const Qml{{struct}} &{{struct|lower}});
    void append(const Qml{{struct}} &{{struct|lower}});
    void update(int row, const Qml{{struct}} &{{struct|lower}});
    void remove(int row);
    void reset(const QList<Qml{{struct}}> data);
    void clear();
public: // from QAbstractListModel    
    virtual int rowCount(const QModelIndex &parent) const;
    virtual QVariant data(const QModelIndex &index, int role) const;
    virtual QHash<int, QByteArray> roleNames() const;    
Q_SIGNALS:
   void countChanged(int count);
private:
    QList<Qml{{struct}}> m_data;
    QHash<int, QByteArray> m_roleNames;
};


