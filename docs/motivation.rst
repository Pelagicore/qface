==========
Motivation
==========

QFace is an attempt to establish one interface description language with an easy to use code generator framework. While QFace as an interface description language is Qt friendly, it is not limited to Qt. The hope is that many projects can agree on this interface language and many interesting generators will be created and we all can learn from how other projects generate code from the same IDL.

The IDL
=======

The IDL uses common API concept such as modules, interfaces, properties, structs and enums/flags. Additional it knows about lists and models. A list is an array of primitive or complex types. A model is an indicator for large data sets which are typical used vian a defined interface or via pagination.

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

The language as such does not provide any support for maps or dictionaries. The keys in dictionaries require a hash which can not always be guaranteed to be available.

Defining APIs
=============

There are many opinions how to define APIs and what is the best way. The hope is if enough people use the same IDL there will be a large set of generators and at the end maybe one common way how to write your QML plugin and export the API.

There are often discussions about if an interface shall be an object or better a singleton. Or if an array shall be exposed as a list or a variant list or even a QmlListProperty or always as a model. Structured data can be exposed using a QVariant or QJSValue or nowadays as a gadget or as a QObject if property notifications are required. Exposing structured data via QObject leads to memory management issues.

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

QFace is purposely designed to have limited features. The goal is to make QFace easy to use with an easy to remember syntax so that people don't need to be experts to write interface files.

QFace does not suppot unions or extending from other interfaces or that a struct extends other structs. If you look for these features than QFace is probably the wring choice.

Limitations
===========

Like other code generation tools, QFace is limited by how much information you can place inside your interface files. In such cases code generation might not make sense and QFace will also help.

QFace allows you to use annotation which can add meta information to the interface files. But the generator needs to be designed to understand this meta information. Only the structure of these annotations are defined not the information they carry. Annotations might help to add information to an interface document to better control the code generation process.
