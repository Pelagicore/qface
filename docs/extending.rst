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


Rule Base Generation
====================

The `RuleGenerator` allows you to extract the documentation rules into an external yaml file. This makes the python script more compact.


.. code-block:: python

    from qface.generator import FileSystem, RuleGenerator
    from path import Path

    here = Path(__file__).dirname()

    def generate(input, output):
        # parse the interface files
        system = FileSystem.parse(input)
        # setup the generator
        generator = RuleGenerator(search_path=here/'templates', destination=output)
        generator.process_rules(here/'docs.yaml', system)

The rules document is divided into several targets. Each target can have an own destination. A target is typical for exampe and app, client, server. Each target can have rules for the different symbols (system, module, interface, struct, enum). An each rule finally consists of a destination modifier, additional context and a documents collection.

.. code-block:: python

    <target>:
        <symbol>:
            context: {}
            destination: ''
            documents:
                <target>:<source>

* ``<target>`` is a name of the current target (e.g. client, server, plugin)
* ``<symbol>`` must be either system, module, interface, struct or enum


Here is an example (``docs.yaml``)

.. code-block:: yaml

    global:
        destination: '{{dst}}'
        system:
            documents:
                '{{project}}.pro': 'project.pro'
                '.qmake.conf': 'qmake.conf'
                'CMakeLists.txt': 'CMakeLists.txt'
    plugin:
        destination: '{{dst}}/plugin'
        module:
            context: {'module_name': '{{module|identifier}}'}
            documents:
                '{{module_name}}.pro': 'plugin/plugin.pro'
                'CMakeLists.txt': 'plugin/CMakeLists.txt'
                'plugin.cpp': 'plugin/plugin.cpp'
                'plugin.h': 'plugin/plugin.h'
                'qmldir': 'plugin/qmldir'
        interface:
            documents:
                '{{interface|lower}}.h': 'plugin/interface.h'
                '{{interface|lower}}.cpp': 'plugin/interface.cpp'
        struct:
            documents:
                '{{struct|lower}}.h': 'plugin/struct.h'
                '{{struct|lower}}.cpp': 'plugin/struct.cpp'


The rule generator adds the ``dst``, ``project`` as also the corresponding symbols to the context automatically. On each level you are able to change the destination or update the context.

