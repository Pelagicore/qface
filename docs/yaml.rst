***********
YAML Primer
***********

This page provides a basic overview of the YAML syntax as used by QFace in the embedded annotations and the external annotations document.

According to the official YAML website, YAML is "a human friendly data serialization standard for all programming languages".

YAML Foundation
===============

For QFace every YAML file is a dictionary of values.

.. code-block:: python

    @singleton: true
    @base: QObject
    interface Heater {
    }

A dictionary in YAML is expressed like this


In an external YAML file the key on the root level is the fully qualified name of the symbol

.. code-block:: YAML

    org.example.Heater:
        singleton: true
        base: QObject

Dictionary
==========

A dictionary is a simple ``key: value`` pair with a colon followed by a space (the space is mandatory).

.. code-block:: yaml

    key: value
    key2: value
    key3:
        key31: value
        key32: value

A nested dictionary can be achieved by a new level of indentation.

An alternate form for a dictionary is this

.. code-block:: yaml

    key3: { key31: value, key32: value }

.. rubric Template

In a template the dictionay can be used as attributes of an object

.. code-block:: jinja

    {% if interface.tags.key == 'value' %}YES{% endif %}

To test is a key exists you can use the key in dictionary form

.. code-block:: jinja

    {% if 'key' in interface.tags %}YES{% endif %}

List
====

A list is an array of values

.. code-block:: yaml

    - item1
    - item2
    - item3:
        - item31
        - item32

A nested list can be created by indenting the list and postfixing the parent entry with a colon.

An alternate form is

.. .. code-block:: yaml

    [ item1, item2, item3: [item31, item32] ]

Comments
--------

YAML only knows line comments. A comment starts with a ``#`` and ends with line.

.. code-block:: yaml

    # this is the key for the value
    key: value

Primitive Types
---------------

YAML understands different primitive types.

.. rubric:: string

YAML understands strings either as an identifier or quoted using ``"`` or ``'``.

You can use code blocks using the ``|`` sign. The block continues until the indentation ends. Or the ``>`` folding block, where each new line is replaced with a space.

.. rubric:: number

YAML understands different number formats, here is a short list of the most important ones

.. code-block:: yaml

    # an integer
    value: 10

    # an hex value
    value: 0xFF

    # a float
    value: 1.01

.. rubric:: boolean

YAML understand different values as true/false.

.. code-block:: yaml

    positive: yes
    positive: true
    negative: no
    negative: false

Besides these words it understand different writing forms (e.g. YES, Yes, Y). Same applies for the negative version.




