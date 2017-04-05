{% set module_name = module.name.lower().replace(".", "_") %}
{% set module_path = module.name_parts|join('/') %}

project({{module_name}})

cmake_minimum_required(VERSION 3.1)

set(CMAKE_CXX_STANDARD 11)

set(INSTALL_PATH "${CMAKE_BINARY_DIR}/imports" CACHE STRING "Path where the plugins are deployed")

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

add_library({{module_name}}_plugin SHARED ${MOC} ${SOURCES})

set(OUTPUT_PATH ${INSTALL_PATH}/{{module_path}})

set_target_properties({{module_name}}_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_PATH}
    RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_PATH}
)

target_link_libraries({{module_name}}_plugin PUBLIC Qt5::Core Qt5::Qml)

add_custom_target(qmldir ALL
    COMMAND ${CMAKE_COMMAND} -E copy
            ${CMAKE_SOURCE_DIR}/qmldir
            ${OUTPUT_PATH}/qmldir
)


