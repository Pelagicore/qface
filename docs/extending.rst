===============
Extending QFace
===============

QFace is easy to use and easy to extend. Your generator is just a small python script using the qface library.

The script iterates over the domain model and writes files using a template language.

See template engine documentation:

* http://jinja.pocoo.org
* http://jinja.pocoo.org/docs/dev/templates


.. code-block:: python

    from qface.generator import FileSystem, Generator

    def generate(input, output):
        # parse the interface files
        system = FileSystem.parse(input)
        # setup the generator
        generator = Generator(searchpath='templates')
        # create a context object
        ctx = {'output': output, 'system': system}
        # apply the context on the template and write the output to file
        generator.write('{{output}}/modules.csv', 'modules.csv', ctx)

This script reads the input directory returns a system object from the domain model. This is used as the root object for the code generation inside the template.

Below is a simple template which geenrates a CSV document of all interfaces, structs and enums.

.. code-block:: jinja

    {% for module in system.modules %}
        {%- for interface in module.interfaces -%}
        INTERFACE, {{module}}.{{interface}}
        {% endfor -%}
        {%- for struct in module.structs -%}
        STRUCT , {{module}}.{{struct}}
        {% endfor -%}
        {%- for enum in module.enums -%}
        ENUM   , {{module}}.{{enum}}
        {% endfor -%}
    {% endfor %}

The template iterates over the domain objects and generates text which is written into a file. The file name is also adjustable using the same template language.
