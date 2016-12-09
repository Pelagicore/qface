Domain Model
============

The domain model resembles the structure of our system as objects. It is build by the parser and is the input into the generator.

It is important to understand the domain model as it is the main input for the template generation.

The IDL is converted into an in memory domain model (see qface/idl/domain.py)

.. code-block:: yaml

    - System
        - Module
            - Import
            - Service
                - Property
                - Operation
                - Event
            - Enum
            - Flag
            - Struct


The domain model is the base for the code generation. You traverse the domain tree and trigger your own code generation.

.. code-block:: python
    from qface.generator import FileSystem

    system = FileSystem.parse_dir('interfaces')

    for module in sytem.modules:
        print(module.name)

        for interfaces in module.interfaces:
            print(interfaces.name)

        for struct in module.structs:
            print(struct.name)


Debug
-----

At any time you can place a debug breakpoint:

.. code-block:: python

    import ipdb; ipd.set_trace()


See https://pypi.python.org/pypi/ipdb


To see the object members just use:

.. code-block:: python

    dir(module) # list all members of module
    help(module) # prints the documentation
