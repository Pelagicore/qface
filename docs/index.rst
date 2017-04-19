=====
QFace
=====

QFace is a flexible Qt API generator. It uses a common IDL format (called QFace interface document) to define an API. QFace comes with a set of predefined generators to generate QML Plugins. QFace can be easily extended with your own generator.

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
   api

Quick Start
===========

QFace is a generator framework but also comes with several reference code generator.

To install qface you need to have python3 installed and typically also pip3

.. code-block:: sh

    pip3 install qface

This installs the python qface library and the two reference generator qface-qtcpp and qface-qtqml.

You can verify that you have qface installed with

.. code-block:: sh

    python3

and then

.. code-block:: python3

    import qface


Custom Generator
----------------

For your own generator you need several ingredients. A QFace interface file here called "sample.qface" a small script which loads and parses the document. And one or more template files, which generate the resulting code.

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

Builtin Generators
------------------

The built-in generators qface-qtcpp and qface-qtqml will generator cpp / qml code from the interface files. The generated code is source code compatible and can be used with the same QML based user interface

.. code-block:: bash

    mkdir cpp-out
    qface-qtcpp sample.qface cpp-out

    mkdir qml-out
    qface-qtqml sample.qface qml-out

The generators can run with one or more input files or folders and generate code for one or more modules. In case of the qtcpp generator the code needs to be open with QtCreator and compiled and installed.

For the QML code the code must just made available to the QML import path.

.. rubric:: See Also

* :doc:`qtcpp`
* :doc:`qtqml`



