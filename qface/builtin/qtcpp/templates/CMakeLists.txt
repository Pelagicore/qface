{% set plugin = module.name.lower().replace(".", "_") %}
project({{plugin}})

cmake_minimum_required(VERSION 3.1)

set(CMAKE_CXX_STANDARD 11)

find_package(Qt5Qml REQUIRED)

set (HEADERS
    generated/qml{{module.module_name|lower}}module.h
{% for interface in module.interfaces %}
    generated/qmlabstract{{interface|lower}}.h
{% endfor %}
{% for struct in module.structs %}
    generated/qml{{struct|lower}}.h
    generated/qml{{struct|lower}}model.h
{% endfor %}
    generated/qmlvariantmodel.h
{% for interface in module.interfaces %}
    qml{{interface|lower}}.h
{% endfor %}
    plugin.h
)


set (SOURCES
    generated/qml{{module.module_name|lower}}module.cpp
{% for interface in module.interfaces %}
    generated/qmlabstract{{interface|lower}}.cpp
{% endfor %}
{% for struct in module.structs %}
    generated/qml{{struct|lower}}.cpp
    generated/qml{{struct|lower}}model.cpp
{% endfor %}
    generated/qmlvariantmodel.cpp
{% for interface in module.interfaces %}
    qml{{interface|lower}}.cpp
{% endfor %}
    plugin.cpp
)

qt5_wrap_cpp(MOC ${HEADERS})

add_library({{plugin}}_plugin SHARED ${MOC} ${SOURCES})

qt5_use_modules({{plugin}}_plugin Qml)
