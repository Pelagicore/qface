===
API
===


Generator API
=============

.. inheritance-diagram:: qface.generator


Generator Class
---------------

.. module:: qface.generator

Provides an API for accessing the file system and controlling the generator


FileSystem Class
----------------

.. autoclass:: qface.generator.FileSystem
    :members:


.. autoclass:: qface.generator.Generator
    :members:


Template Domain API
===================

.. module:: qface.idl.domain

This API is exposed to the Jinja template system.

.. inheritance-diagram:: qface.idl.domain

High Level Classes
------------------

.. autoclass:: qface.idl.domain.System
    :members:

.. autoclass:: qface.idl.domain.Module
    :members:
    :show-inheritance:


Interface Related Classes
-------------------------

.. autoclass:: qface.idl.domain.Interface
    :members:


.. autoclass:: qface.idl.domain.Operation
    :members:

.. autoclass:: qface.idl.domain.Parameter
    :members:

.. autoclass:: qface.idl.domain.Property
    :members:


Struct Related Classes
----------------------

.. autoclass:: qface.idl.domain.Struct
    :members:
    :show-inheritance:


.. autoclass:: qface.idl.domain.Field
    :members:
    :show-inheritance:

.. rubric:: Enum/Flag Related Classes

.. autoclass:: qface.idl.domain.Enum
    :members:
    :show-inheritance:

.. autoclass:: qface.idl.domain.EnumMember
    :members:
    :show-inheritance:


Base Classes
------------

.. autoclass:: qface.idl.domain.Symbol
    :members:
    :show-inheritance:

.. autoclass:: qface.idl.domain.TypedSymbol
    :members:
    :show-inheritance:

.. autoclass:: qface.idl.domain.TypeSymbol
    :members:
    :show-inheritance:
