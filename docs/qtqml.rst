=====================
Qt QML Code Generator
=====================

The Qt QML Code generator creates a pure QML implementation of the provided QFace interface files. From the QML perspective it is API compatible. This means an HMI written in QML can be run against plugins generated from the QtCPP code generator and QtQML code generator.

This allows developers to start early with an QML only implementation and later switch to an QtCPP based implementation, without changing the HMI code.

.. note::

    As the HMI is limited to the API there might still be differences in behavior of the two implementations. This is in the nature of APIs and might lead to different result.

For each module the generator creates a module JS file, which contains the enums and factory methods for the structure. A structure is in the pure QML implementation just a JS object with correct attributes set.

The interfaces are generated as QtObject types and contain the typical properties, operations and signals.

.. rubric:: Code Generation

.. code-block:: yaml

    for each module:
        - qmldir
        - {{module}}Module.js
        - for each interface:
            - interface.qml


