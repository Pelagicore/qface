# Usage

There is a central client to interface the commands for generation, called cli.

To use an existing generator just provide the path to the generator script.

    ./cli.py generator --generator generator/csv --input input --output output

You can also create a YAML configuration file (e.g csv.yaml):

    generator: generator/csv
    input: input
    output: output

And then call the client with:

    ./cli.py generate --runner csv.yaml

To enable auto-live reloading just use the monitor target:


    ./cli.py generator_monitor --runner csv.yaml

This will observe the generator folder and the input folder for changes and re-run the generator.

# Grammar

The IDL grammar is described in the grammar file (see qface/parser/idl/T.g4)

    package <identifier> <version>;

    [import <identifier> <version>];

    interface <identifier> {
        (readonly) <type> <attribute>;
        <type> <operation>([type name]);
        event <type> <operation>([type name]);
        list<type> <attribute>;
        model<type> <attribute>;
    }

    enum <identifier> {
        <name> = <value>
    }

    flag <identifier> {
        <name> = <value>
    }

    struct <identifier> {
        <type> <name>;
    }


# Domain Model

The IDL is converted into an in memory domain model (see qface/idl/domain.py).

    System
        Package
            Import
            Service
                Attribute
                Operation
            Enum
            Struct

The domain model is the base for the code generation.

# Code Generation

The code generation is driven by a small script which iterates over the domain model and writes files using a template language (see http://jinja.pocoo.org) and espcially the template designer documentation (http://jinja.pocoo.org/docs/dev/templates/).

    from qface.generator import FileSystem, Generator

    def generate(input, output):
        system = FileSystem.parse_dir(input)
        generator = Generator(searchpath='templates')
        ctx = {'output': output, 'system': system}
        generator.write('{{output}}/packages.csv', 'packages.csv', ctx)

This script reads the input directory returns a system object form the domain model. This is used as the root object for the code generation inside the template language.

    {% for package in system.packages %}
        {%- for interface in package.interfaces -%}
        SERVICE, {{package}}.{{interface}}
        {% endfor -%}
        {%- for struct in package.structs -%}
        STRUCT , {{package}}.{{struct}}
        {% endfor -%}
        {%- for enum in package.enums -%}
        ENUM   , {{package}}.{{enum}}
        {% endfor -%}
    {% endfor %}

The tempate iterates over the domain objects and generates text which is written into a file. The file name is also adjustable using the same template language.
