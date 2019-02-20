*********
Extending
*********

QFace is easy to use and easy to extend with your own generator. The standard way is to write a rules document to control the code generation. The more complicated path is to write your generator using just a small python script which uses qface as library.

Rules Extensions
================

The rules extension uses a YAML based document to control the code generation. The document is structured roughly like this:

.. code-block:: yml

    <scope>:
        when: <feature-list>
        context: <context map update>
        path: <target path prefix>
        source: <source prefix>
        <qualifier>:
            when: <feature-list>
            context: <context map update>
            path: <target path prefix>
            source: <source prefix>
            documents:
                - <target>: <source>
            preserved:
                - <target>: <source>


.. rubric:: `scope` entry

Scope is a logical distribution of generator. For example if you write a client/server generator you may want to have a ``client`` and ``server`` scope. This enables you also to switch a scope off using the ``when`` condition.

.. rubric:: `qualifier` entry

The qualifier defines the domain model type this code generation section shall be applied to. Valid qualifiers are ``system``, ``module``, ``interface``, ``struct`` and ``enum``.


.. rubric:: `when` entry

The  `when` entry defines a condition when this part of the code generation is enabled. For example you may have some code generation parts, which create a scaffold project. By passing in the scaffold flag or by  enabling the scaffold feature this part would then also be evaluated. By default when is true.

.. rubric:: `context` entry

The contexct map allows you to extend the cotnext given to the template. Each context key will then accessible in the template.

.. rubric:: `path` entry

The path is the path appended to the target directory. So the full export path for a template is ``<target>/<path>/<template>``.

.. rubric:: `source` entry

The source prefixed to the template name. For example to not to repeat the ``server`` folder for the next templates you can set the ``source`` to ``server``.


.. rubric:: `documents` entry

The documents section is a list of target, source templates. The source defines the template document used to produce the target document. The target document can have a fully qualified template syntax, for example ``{{interface}}.h``, where the interface name is looked up using the given context. When generating existing documents will be overriden.

.. rubric:: `preserve` entry

Very similar to the documents section. The only difference is that existing documents will be preserved. You can overrule this using the ``--force`` command line option.

Preserved is useful when generated document shall be edited by the user and a new run of the generator shall not overwrite (preserve) the edited document.

.. rubric:: Example

Below is a more complex rules document from the qtcpp generator using one scope called ``project``.

.. code-block:: yaml

    project:
        system:
            documents:
                - '{{project}}.pro': 'project.pro'
                - '.qmake.conf': 'qmake.conf'
                - 'CMakeLists.txt': 'CMakeLists.txt'
        module:
            path: '{{module|identifier}}'
            documents:
                - 'CMakeLists.txt': 'plugin/CMakeLists.txt'
                - 'qmldir': 'plugin/qmldir'
                - 'generated/generated.pri': 'plugin/generated/generated.pri'
                - 'generated/{{module|identifier}}_gen.h': 'plugin/generated/module.h'
                - 'generated/{{module|identifier}}_gen.cpp': 'plugin/generated/module.cpp'
                - 'docs/plugin.qdocconf': 'plugin/docs/plugin.qdocconf'
                - 'docs/plugin-project.qdocconf': 'plugin/docs/plugin-project.qdocconf'
                - 'docs/docs.pri': 'plugin/docs/docs.pri'
            preserve:
                - '{{module|identifier}}.pro': 'plugin/plugin.pro'
                - 'plugin.cpp': 'plugin/plugin.cpp'
                - 'plugin.h': 'plugin/plugin.h'
        interface:
            preserve:
                - '{{interface|lower}}.h': 'plugin/interface.h'
                - '{{interface|lower}}.cpp': 'plugin/interface.cpp'


Script Extensions
=================

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

The rules document is divided into several targets. Each target can have an own destination. A target is typical for example and `app`, `client` or `server`. Each target can have rules for the different symbols (system, module, interface, struct, enum). An each rule finally consists of a destination modifier, additional context and a documents collection.

.. code-block:: python

    <target>:
        <symbol>:
            context: { <key>: <value> }
            destination: <path>
            documents:
                <target>:<source>
            preserve:
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


.. rubric:: Features

The rules document allows to conditional write files based on a feature set. The feature set must be a set of tags indicating the features which will then be checked in the ``when`` section of a rule. The ``when`` tag needs to be a list of feature switched.

The features are passed to the generator in your custom generator code. The existence of a feature tells the rules engine to check if a ``when`` section exists conditionally execute this rule.

.. code-block:: yaml

    plugin:
        when: [plugin_enabled]
        destination: '{{dst}}/plugin'
        module:
            ...

Here the plugin rule will only be run when the feature set contains a 'plugin_enabled' string.

.. rubric:: Preserving Documents

Documents can be moved to the ``preserve`` tag to prevent them to be overwritten. The rules documents has an own marker for this called ``preserve``. This is the same dictionary of target/source documents which shall be be marked preserved by the generator.


.. code-block:: yaml

    plugin:
        interface:
            documents:
                '{{interface|lower}}.h': 'plugin/interface.h'
            preserve:
                '{{interface|lower}}.cpp': 'plugin/interface.cpp'

In the example above the preserve listed documents will not be overwritten during a second generator run and can be edited by the user.

.. rubric:: Destination and Source

The ``destination`` tag allows you to specify a prefix for the target destination of the document. It should always contain the ``{{dst}}`` variable to be placed inside the project folder.

The ``source`` tag specifies a prefix for the templates resolving. If the template name starts with a ``/`` the prefix will be ignored.

Destination and source tags are allowed on the target level as also on each system, module and other symbol levels. A tag on a parent symbol will be the default for the child symbols.

.. rubric:: Implicit symbol hierarchy

This is the implicit logical hierarchy taken into account:

.. code-block:: xml

    <target>
        <system>
            <module>
                <interface>
                <struct>
                <enum>

Typical you place the destination prefix on the module level if your destination depends on the module symbol. For generic templates you would place the destination on the system level. On the system level you can not use child symbols (such as the module) as at this time these symbols are not known yet.

Parsing Documentation Comments
==============================

The comments are provided as raw text to the template engine. You need to parse using the `parse_doc` tag and the you can inspect the documentation object.

See below for a simple example

.. code-block:: html

    {% with doc = property.comment|parse_doc %}
    \brief {{doc.brief}}

    {{doc.description}}
    {% endwith %}

Each tag in the JavaDoc styled comment, will be converted into a property of the object returned by `parse_doc`. All lines without a tag will be merged into the description tag.


Language Profiles
=================


QFace supports the notion of profile. A profile is a set of features supported by the named profile. The intention of a profile is to make it easier for generator writers to stick to a limited set of language features, also if the overall language is evolving.

Currently there exists three language profiles:

* Micro - A limited set of languages features. The base profile. It does not allow importing of other modules or extending an interface, neither does it support maps.
* Advanced - Builds upon micro and allows imports, maps, interface extension.
* Full - Builds up on advanced and will also contain experimental language features.

The current features defined are:
- const oeprations
- const properties
- imports
- maps
- interface extensions

The profiles and features are defined in the `qface.idl.profile` module.

.. code-block:: py

    from qface.generator import FileSystem
    from qface.idl.profile import EProfile

    system = FileSystem.parse(input=input, profile=EProfile.MICRO)

