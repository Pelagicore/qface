=====
QFace
=====

QFace is a flexible API generator inspired by the Qt API idioms. It uses a common IDL format (called QFace interface document) to define an API. QFace is optimized to write a custom generator based on the common IDL format.

Several code generators for common use cases have already been implemented. These can be used as is or can be used as a base for a custom generator.

.. toctree::
   :maxdepth: 1

   motivation
   usage
   builtin
   grammar
   annotations
   yaml
   json
   domain
   extending
   script
   api


Features
========

The list fo features is plit between features which are based on the chosen IDL and features which are provided by the generator itself.

.. rubric:: IDL Features

- Common modern IDL
- Scalable through modules
- Structure through structs, enums, flags
- Interface API with properties, operations and signals
- Annotations using YAML syntax
- Documentable IDL

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

    python3

and then

.. code-block:: python3

    import qface


Custom Generator
----------------

For your own generator you need several ingredients. A QFace interface file (here called "sample.qface"), a small script which loads and parses the document (generator.py) and one or more template files, used by the script to generate the resulting code.

The QFace document could look like this

.. code-block:: thrift

    // sample.qface
    module org.example 1.0

    interface Echo {
        string echo(string msg);
    }


Your generator can now parse the documents and call the templates

.. code-block:: python3

    // generator.py
    from qface.generator import FileSystem, Generator

    system = FileSystem.parse('sample.qface')
    generator = Generator('./templates')
    for module in system.modules:
        ctx = { 'module' : module }
        generator.write('{{module}}.txt', 'module.tpl', ctx)

The final piece is the template to parameterize the output in this case called "module.tpl"

.. code-block:: jinja

    // templates/module.tpl
    {% for interface in module.interfaces %}
    {{module.name}}
    {% endfor %}

Now you can simple call your script

.. code-block:: bash

    python3 generator.py

And a "org.example.txt" file named after the module should be generated.

.. rubric:: See Also

* :doc:`extending`
* :doc:`grammar`
* :doc:`domain`
* :doc:`api`

Bundled Generators
------------------

QFace has some generators which are bundled with the QFace library. They live in their own repositories. These generators are documented in their respective repositories.

.. rubric:: See Also

* :doc:`qtcpp`
* :doc:`qtqml`



