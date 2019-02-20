Domain Model
============

The domain model resembles the structure of our system as objects. It is build by the parser and is the input into the generator.

It is important to understand the domain model as it is the main input for the template generation.

The IDL is converted into an in memory domain model (see qface/idl/domain.py)

.. code-block:: yaml

    - System
        - Module
            - Import
            - Interface
                - Property
                - Operation
                - Signal
            - Struct
            - Enum
            - Flag

The domain model is the base for the code generation. You traverse the domain tree and trigger your own code generation. Below you see a python example to traverse the model. Normally you do not need todo this, as the rules generator does the traversing for you.

.. code-block:: python

    from qface.generator import FileSystem

    system = FileSystem.parse('./interfaces')

    for module in system.modules:
        print(module.name)

        for interfaces in module.interfaces:
            print(interfaces.name)

        for struct in module.structs:
            print(struct.name)


The rules generator calls the template directive for each domain element found and it is up to the template to place the code in the right place.

.. code-block:: yml

    project:
        system:
            documents:
                - '{{system}}.txt': 'system.txt'
        module:
            documents:
                - '{{module}}.txt': 'module.txt'
        interface:
            documents:
                - '{{interface}}.txt': 'interface.txt'
        struct:
            documents:
                - '{{struct}}.txt': 'struct.txt'
        enum:
            documents:
                - '{{enum}}.txt': 'enum.txt'
