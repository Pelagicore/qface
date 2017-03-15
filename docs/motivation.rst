==========
Motivation
==========

QFace is an attempt to establish one interface description language with an easy to use code generator framework. While QFace as an interface description language is Qt friendly, it is not limited to Qt. The hope is that many projects can agree on this interface language and many interesting generators will be created and we all can learn from how other projects generate code from the same IDL.

The IDL
=======

The IDL uses common API concept such as modules, interfaces, properties, structs and enums/flags. Additionally it knows about lists and models. A list is an array of primitive or complex types. A model is an indicator for large data sets which are typical used via a defined interface or via pagination.

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

Primitive Types

* bool
* int
* real
* string
* var

Complex Types

* Interface
* Struct
* Enum
* Flag
* Array
* Model

The language as such does not provide any support for maps or dictionaries. The reason for not providing a map container type is that keys in dictionaries requires a hash which can not always be guaranteed to be available in complex types.

Why another IDL
===============

There exists many IDLs. Most of them are bound to a certain technology or library or are limited for a specific use. Only a few IDL exists which are independent from a technology. From these few which are known to the author none satisfied the requirement from the author to be Qt compatible and easy to use. Also the IDL should be easy to use and easy to be install and to be extendable. The unique mix of technologies used in QFace allows it to provide a solid stable IDL with a powerful generation framework.


Defining APIs
=============

There are many opinions how to define APIs and what is the best way. The porposal of QFace is that is many project find QFace useful and use the same IDL there will be a large set of generators and at the end APIs can be compared and unified also if they will be used with different technologies.

Even inside on e technolgy there are often discussions about how an interface shall be coded. QFace allows the different parties to create their own generators based on the same API. Ideally at the end the knowledge how an interface shall be coded will reside in the provided generator.

Large Projects
==============

In larger projects there is the need to make available to QML a large set of operating services. It is less about defining new visual items in C++, more about creating an abstraction of a service and make it available to the HMI developer inside QML.

This can be a challenge when you create many of these plugins and in the middle of the project you figure out you have issues with your current design. Or if the customer in the next project wants to use a different HMI technology. All the knowledge is inside these plugins.

With QFace these companies can be certain that QFace does not lock them into the HMI technology and smaller design issues can be fixed by fixing the generator.

Remote Services
===============

Some projects use network communication to communicate from the HMI to the services, which might run on a different process or event networked device. QFace was not designed for remote services as it does not define any storage types (e.g. int32, int16, int64), it  only knows an int and does not define how large the int shall be. For this QFace needs to rely on the author of the generators to have a defined protocol to exchange data.

Complex APIs
============

QFace is purposely designed to have limited features. The goal is to make QFace easy to use with an easy to remember syntax so that you don't need to be an expert to write interface files.

QFace does not suppot unions or extending from other interfaces or that a struct extends other structs. If you look for these features than QFace is probably the wrong choice.

Limitations
===========

Like other code generation tools, QFace is limited by how much information you can place inside your interface files. In such cases code generation might not make sense and QFace will also help.

QFace allows you to use annotation which can add meta information to the interface files. But the generator needs to be designed to understand this meta information. Only the structure of these annotations are defined not the information they carry. Annotations might help to add information to an interface document to better control the code generation process.
