==========
Motivation
==========

QFace is an attempt to establish a common interface description language with an easy to use code generator framework. While QFace as an interface description language which is Qt friendly, it is not limited to Qt usage. The vision is that many projects can agree on this interface language and many different generators will be created. In the end we all can learn from how other projects generate code from the same IDL.

The IDL
=======

The IDL uses common API concept such as ``modules``, ``interfaces``, ``properties``, ``structs`` and ``enums``/``flags``. Additionally it knows about ``lists``, ``maps`` and ``models``. A list is an array of primitive or complex types. A map is an associative array of key/value pairs. A model is an indicator for large data sets which are typically used using a streaming concept, e.g. via a defined interface or via pagination.

.. code-block:: js

    module org.example 1.0

    interface Echo {
        string message;
        void echo(string message);
        signal broadcast(string message);
        Status status;
    }

    enum Status {
        Null, Loading, Ready, Error
    }


The data types provided by QFace can be divided into primitive and complex types:

.. rubric:: Primitive Types

The primiteve types are mostly modeled after the JSON data types (see https://www.json.org/).

All exact data types (e.g. 32bit, 64bit, etc depend on the generator the IDL).

* ``bool`` - true/false
* ``int`` - represents integer type
* ``real`` - floating point number
* ``string`` - unicode string
* ``var`` - placeholder for a data type

.. rubric:: Complex Types

A complex type is a composition of other types and add specific semantic to the type.

* ``Interface`` - collection of properties, operations and signals
* ``Struct`` - typed data package
* ``Enum`` - enumeration of integer values
* ``Flag`` - enumeration with n^2 values
* ``List`` - array of primitive or complex data types
* ``Map`` - collection of primitive or complex value. Key type is defined by generator. E.g. string is recommended.
* ``Model`` - A stream of primitive or complex data values.


Why another IDL
===============

Many IDLs are already in existence. But most of them are bound to a certain technology or library or are limited for a specific use. Only a few IDLs exist which are independent from a technology. From these few technology independent IDLs which are known to the author satisfied the requirement to be Qt compatible and easy to use. Also the IDL should be easy to install and be extendable. The unique mix of technologies used in QFace allows it to provide a solid stable IDL with a powerful generation framework. - The base for your own code generator.


Defining APIs
=============

There are many opinions how to define APIs and what would be the best way. The idea of QFace is that many projects find the IDL useful and use it to create their own code generator. Consequently, there will be a large set of generators and finally APIs can be compared and unified, even if they will be used with different technologies.

Inside one technology area there are often discussions between developers or teams about how an interface shall be coded. QFace allows the different parties to create their own generators based on the same API. Ideally at the end the knowledge how an interface shall be best coded will reside in the provided generator.

Large Projects
==============

In larger projects there is the need to make a large set of operating services available to an user interface layer. It is less about defining new visual items in C++, more about creating an abstraction of a service and make it available to the UI developer.

This can be a challenge when you create many plugins and in the middle of the project you figure out that you have issues with your current design or if the customer in the next project wants to use a different HMI technology. All the knowledge is inside these plugins.

With QFace these companies can be ensured that QFace does not lock them into the UI technology and smaller API design issues can be fixed by fixing the used code generator.

Remote Services
===============

Some projects use network communication to communicate from the HMI to the services, which might run on a different process or even a networked device. QFace was not designed for remote services as it does not define any storage types (e.g. int32, int16, int64), it  only knows an ``int`` and does not define how large the ``int`` shall be. For this QFace needs to rely on the author of the generators to have a defined protocol to exchange data using QFace common data types.

Complex APIs
============

QFace is purposely designed to have limited features. The goal is to make QFace easy to use with an easy to remember syntax so that you don't need to be an expert to write interface files.

QFace does not support unions or structs that extend other structs. If you look for these features, QFace is probably the wrong choice.

Limitations
===========

Like other code generation tools, QFace is limited by how much information you can place inside your interface files. In excessive cases code generation might not make sense and hence QFace will also not help you.

QFace allows you to use annotations which can add meta information to the interface files. But the generator needs to be designed to understand this meta information. QFace only defined the the structure of these annotations not the information and semantic they carry. Annotations might help you to add information to an interface document to better control the code generation process.
