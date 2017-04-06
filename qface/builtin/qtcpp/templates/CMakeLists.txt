{% set module_name = module.name.lower().replace(".", "_") %}
{% set module_path = module.name_parts|join('/') %}

project({{module_name}})

cmake_minimum_required(VERSION 3.1)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_AUTOMOC ON)

set(INSTALL_PATH "${CMAKE_BINARY_DIR}/imports" CACHE STRING "Path where the plugins are deployed")

find_package(Qt5Core REQUIRED)
find_package(Qt5Qml REQUIRED)

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

add_library({{module_name}}_plugin SHARED ${SOURCES})

set(OUTPUT_PATH ${INSTALL_PATH}/{{module_path}})

set_target_properties({{module_name}}_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_PATH}
    RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_PATH}
)

target_link_libraries({{module_name}}_plugin PUBLIC Qt5::Core Qt5::Qml)
configure_file(${CMAKE_SOURCE_DIR}/qmldir ${OUTPUT_PATH}/qmldir COPYONLY)
