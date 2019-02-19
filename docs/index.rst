=====
QFace
=====

* see https://github.com/pelagicore/qface

QFace is a flexible API generator inspired by the Qt API idioms. It uses a common IDL format (called QFace interface document) to define an API. QFace is optimized to write a custom generator based on the common IDL format.

Several code generators for common use cases have already been implemented. These can be used as is or can be used as a base for a custom generator.

.. toctree::
   :maxdepth: 1

   motivation
   usage
   reference
   grammar
   annotations
   yaml
   json
   domain
   extending
   rules
   api


Features
========

The list fo features is split between features which are based on the chosen IDL and features which are provided by the generator itself.

.. rubric:: IDL Features

- Common modern IDL
- Scalable through modules
- Structured data through structs, enums, flags
- Interface API with properties, operations and signals
- Annotations using YAML syntax
- Fully documentable

.. rubric:: Generator Features

- Easy to install using python package manager
- Designed to be extended
- Well defined domain objects
- Template based code generator
- Simple rule based code builder
- Well documented

Quick Start
===========

QFace is a generator framework and is bundled with several reference code generators.

To install qface you need to have python3 installed and typically also pip3

.. code-block:: sh

    pip3 install qface

This installs the python qface library onto your system.

You can verify that you have qface installed with

.. code-block:: sh

    qface --help


Custom Generator
----------------

To write a custom generator it is normally enough to write a generator rules and the used templates. We use a QFace interface file (here called "sample.qface") as an example.

The QFace document could look like this

.. code-block:: thrift

    // interfaces/sample.qface
    module org.example 1.0

    interface Echo {
        string echo(string msg);
    }


We need now to write our templates for the code generation. In our example we would simple print out for each module the interfaces and it's operations.

.. code-block:: jinja

    {# templates/module.tpl #}
    {% for interface in module.interfaces %}
    {{module}}.{{interface}}
    {% endfor %}

This will write for each interface in the module the text ``<module>.<interface>``. The rules file will define what shall be generated and where.

.. code-block:: yaml

    # qface-rules.yaml

    project:
      module:
        documents:
          - {{module}}.csv: module.tpl

The first entry defined a scope (e.g. project). Then for each module we geenrated documents. We use the module.tpl document from the templates folder and generate a CSV document based on the module name.

Now you can simple call your rules document

.. code-block:: bash

    qface --rules qface-rules.yaml --target output interfaces

And a "org.example.csv" file named after the module should be generated.

.. rubric:: See Also

* :doc:`extending`
* :doc:`grammar`
* :doc:`domain`
* :doc:`api`

Generators
----------

QFace has several generator maintained by the qface team. They are maintained and documented in their own repositories.

* https://github.com/pelagicore/qface-qtcpp
* https://github.com/pelagicore/qface-qtqml




