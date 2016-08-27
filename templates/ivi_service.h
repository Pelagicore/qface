/****************************************************************************
**
** Copyright (C) 2016 Pelagicore AG
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtIvi module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL-QTAS$
** Commercial License Usage
** Licensees holding valid commercial Qt Automotive Suite licenses may use
** this file in accordance with the commercial license agreement provided
** with the Software or, alternatively, in accordance with the terms
** contained in a written agreement between you and The Qt Company.  For
** licensing terms and conditions see https://www.qt.io/terms-conditions.
** For further information use the contact form at https://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
** SPDX-License-Identifier: LGPL-3.0
**
****************************************************************************/

#ifndef {{service|upper}}_H
#define {{service|upper}}_H

#include <QtIviCore/QIviAbstractZonedFeature>
#include <QtIviCore/QIviProperty>
#include <QtIviVehicleFunctions/qtivivehiclefunctionsglobal.h>

QT_BEGIN_NAMESPACE

class QIviClimateControlBackendInterface;
class QIviClimateControlPrivate;

static const QLatin1String QIviStringClimateControlInterfaceName("com.qt-project.qtivi.ClimateControl");

class Q_QTIVIVEHICLEFUNCTIONS_EXPORT QIvi{{service}} : public QIviAbstractZonedFeature
{
    Q_OBJECT
{% for attribute in service.attributes %}
    Q_PROPERTY(QIviProperty* {{attribute}} READ {{attribute}}Property CONSTANT)
{% endfor %}

public:
{% for enum in package.enums %}
    enum {{enum}} {
    {% for member in enum.members %}
        {{member}} = {%if enum.is_flag%}{{member.value|hex}}{%else%}{{member.value}}{%endif%}{% if not loop.last %},
        {% else %}

        {% endif %}
    {% endfor %}
    };
    {% if enum.is_flag %}
    Q_DECLARE_FLAGS({{enum}}s, {{enum}})
    Q_FLAG({{enum}}s)
    {% else %}
    Q_ENUM({{enum}})
    {% endif %}

{% endfor %}
    QIvi{{service}}(QObject* parent=Q_NULLPTR);
    ~QIvi{{service}}();
{% for attribute in service.attributes %}
    {{attribute|returnType}} {{attribute}}() const;
    QIviPropertyAttribute<{{attribute.type}}> {{attribute}}Attribute() const;
    QIviProperty* {{attribute}}Property() const;
{% endfor %}
{% for operation in service.operations %}
    Q_INVOKABLE {{operation|returnType}} {{operation}}();
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

#endif
