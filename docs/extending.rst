***************
Extending QFace
***************

QFace is easy to use and easy to extend. Your generator is just a small python
script using the qface library.

The script iterates over the domain model and writes files using a template
language.

See template engine documentation:

* http://jinja.pocoo.org
* http://jinja.pocoo.org/docs/dev/templates


.. code-block:: python

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

This script reads the input directory returns a system object from the domain
model. This is used as the root object for the code generation inside the
template. The  context object is applied to the file path as also on the named
template document. The output of the template is then written to the given file
path.

Below is a simple template which generates a CSV document of all interfaces,
structs and enums.

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

The template code iterates over the domain objects and generates text using a
mixture of output blocks ``{{}}`` and control blocks ``{%%}``.
