==========
Motivation
==========

QFace is an attempt to establish one interface description language with an easy to use code generator framework. While QFace as an interface description language is Qt friendly, it is not limited to Qt. The hope is that many projects can agree on this interface language and many interesting generators will be created and we all can learn from how other projects generate code from the same IDL.

The IDL
=======

The IDL uses common API concept such as modules, interfaces, properties, structs and enums/flags. Additionally it knows about lists, maps and models. A list is an array of primitive or complex types. A map is an associative array of key/value pairs. A model is an indicator for large data sets which are typically used via a defined interface or via pagination.

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
* List
* Map
* Model


Why another IDL
===============

Many IDLs are already in existence. Most of them are bound to a certain technology or library or are limited for a specific use. Only a few IDLs exist which are independent from a technology. From these few which are known to the author none satisfied the requirement from the author to be Qt compatible and easy to use. Also the IDL should be easy to install and be extendable. The unique mix of technologies used in QFace allows it to provide a solid stable IDL with a powerful generation framework.


Defining APIs
=============

There are many opinions how to define APIs and what the best way is. The idea of QFace is that many projects find it useful and use the same IDL. Consequently, there will be a large set of generators and finally APIs can be compared and unified also if they will be used with different technologies.

Even inside one technology there are often discussions about how an interface shall be coded. QFace allows the different parties to create their own generators based on the same API. Ideally at the end the knowledge how an interface shall be coded will reside in the provided generator.

Large Projects
==============

In larger projects there is the need to make a large set of operating services available to QML. It is less about defining new visual items in C++, more about creating an abstraction of a service and make it available to the HMI developer inside QML.

This can be a challenge when you create many of these plugins and in the middle of the project you figure out that you have issues with your current design or if the customer in the next project wants to use a different HMI technology. All the knowledge is inside these plugins.

With QFace these companies can be certain that QFace does not lock them into the HMI technology and smaller design issues can be fixed by fixing the generator.

Remote Services
===============

Some projects use network communication to communicate from the HMI to the services, which might run on a different process or even a networked device. QFace was not designed for remote services as it does not define any storage types (e.g. int32, int16, int64), it  only knows an int and does not define how large the int shall be. For this QFace needs to rely on the author of the generators to have a defined protocol to exchange data.

Complex APIs
============

QFace is purposely designed to have limited features. The goal is to make QFace easy to use with an easy to remember syntax so that you don't need to be an expert to write interface files.

QFace does not support unions or structs that extend other structs. If you look for these features, QFace is probably the wrong choice.

Limitations
===========

Like other code generation tools, QFace is limited by how much information you can place inside your interface files. In excessive cases code generation might not make sense and hence QFace will also not help.

QFace allows you to use annotations which can add meta information to the interface files. But the generator needs to be designed to understand this meta information. Only the structure of these annotations are defined not the information they carry. Annotations might help to add information to an interface document to better control the code generation process.
