=====
Usage
=====

Concept
=======

QFace requires one or more IDL files as input file and a generator to produce output files. The IDL files are named QFace interface documents.

.. figure:: qface_concept.jpg

To use QFace you need to write your own generator. A generator is a small python script which reads the QFace document and writes code using template files.

.. code-block:: python

    # gen.py
    from qface.generator import FileSystem, Generator

    def generate(input, output):
        # parse the interface files
        system = FileSystem.parse(input)
        # setup the generator
        generator = Generator(search_path='templates')
        # create a context object
        ctx = {'output': output, 'system': system}
        # apply the context on the template and write the output to file
        generator.write('{{output}}/modules.csv', 'modules.csv', ctx)

    # call the generation function
    generate('sample.qface', 'out')


.. code-block:: sh

    python3 gen.py


Code Generation Principle
=========================

The code generation is driven by a small script which iterates over the domain model and writes files using the Python Jinja template language. Refer to http://jinja.pocoo.org and particularly the template designer documentation at http://jinja.pocoo.org/docs/dev/templates/.

.. code-block:: python

    from qface.generator import FileSystem, Generator

    def generate(input, output):
        system = FileSystem.parse(input)
        generator = Generator(searchpath='templates')
        ctx = {'output': output, 'system': system}
        generator.write('{{output}}/modules.csv', 'modules.csv', ctx)


This script reads the input directory and returns a system object from the domain model. This is used as the root object for the code generation inside the template language.

.. code-block:: jinja

    {% for module in system.modules %}
        {%- for interface in module.interfaces -%}
        SERVICE, {{module}}.{{interface}}
        {% endfor -%}
        {%- for struct in module.structs -%}
        STRUCT , {{module}}.{{struct}}
        {% endfor -%}
        {%- for enum in module.enums -%}
        ENUM   , {{module}}.{{enum}}
        {% endfor -%}
    {% endfor %}

The template iterates over the domain objects and generates text which is written into the output file. Using the generator write method ``generator.write(path, template, context)`` the output file path can be specified.
