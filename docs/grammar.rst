=============
QFace Grammar
=============

QFace (Qt interface language) is an Interface Description Languge (IDL). While it is primarily designed to define an interface between Qt, QML and C++, it is intended to be flexible enough also to be used in other contexts.

.. code-block:: html

    module <module> <version>
    import <module> <version>

    interface <Identifier> {
        <type> <identifier>
        <type> <operation>(<parameter>*)
        signal <signal>(<parameter>*)
    }

    struct <Identifier> {
        <type> <identifier>;
    }

    enum <Identifier> {
        <name> = <value>,
    }

    flag <Identifier> {
        <name> = <value>,
    }

A QFace document always describes one module. Each document can contain one or more interfaces, structs, flags or enums. Each document can import other modules using the import statement.


Module
======

A module is identified name. A module should be normally a URI where all parts are lowercase (e.g. `entertainment.tuner`). A module may import other modules with the primary purpose being to ensure that dependencies are declared inside the QFace file.

Types
-----

Types are either local and can be references simply by its name, or they are from external module in this case they need to be referenced with the fully qualified name (``module + '.' + name``). A type can be an interface, struct, enum or flag.

A module consist of either one or more interfaces, structs and enums/flags. They can come in any number or combination. The interface is the only type which can contain operations and signals. The struct is merely a container to transport structured data. An enum/flag allows the user to encode information used inside the struct or interface as datatype.

The QFace does not allow to extend interfaces. It is by design kept simple.

Below is an example of a QFace file.

.. code-block:: js

    module entertainment.tuner 1.0;

    import common 1.0

    /*! Service Tuner */
    interface Tuner {
        /*! property currentStation */
        readonly Station currentStation;
        /*! operation nextStation */
        void nextStation();
        /*! operation previousStation */
        void previousStation();
        /*! operation updateCurrentStation */
        void updateCurrentStation(int stationId);

        list<int> primitiveList;
        list<Station> complexList;
        model<int> primitiveModel;
        model<Station> complexModel;
    }

    /*! enum State */
    enum State {
        /*! value State.Null */
        Null=0,
        /*! value State.Loading */
        Loading=1,
        /*! value State.Ready */
        Ready=2,
        /*! value State.Error */
        Error=3
    }

    /*! enum Waveband */
    enum Waveband {
        /*! value Waveband.FM */
        FM=0,
        /*! value Waveband.AM */
        AM=1
    }

    flag Features {
        Mono = 0x1,
        Stereo = 0x2,
    }

    /*! struct Station */
    struct Station {
        /*! member stationId */
        int stationId;
        /*! member name */
        string name;
        /*! last time modified */
        common.TimeStamp modified;
    }


Tags / Annotations
==================

Tags allows an interface author to extend the existing grammar with additional meta information, called tags, aka annotations. One or several annotations can stand in from of a module, interface, struct or enum. They are also allowed before an operation, property or signal. Everywhere where a documentation comment is allowed you can also add annotations.

An annotation looks like this::

    @service(port=12345)
    interface Tuner {
    }

A annotation format is very similar to an operation signature prefixed with an `@` sign and no return value.

The annotation are available later when navigating the domain model.

.. note:: QFace does not specify specific annotations, but defines just the annotation format. The set of annotations supported must be defined and documented by the generator.

.. rubric:: Annotation Documents

QFace allows also to specify these annotations in external documents using the `YAML` syntax. For this you need to create a document with the same name as the QFace document but with the extension `.yaml`. It should have roughly the following format

.. code-block:: yaml

    com.pelagicore.ivi.Tuner:
        service:
            port: 12345

On the root level should be a fully qualified name of a symbol. The symbol will be looked up and the following annotation information merged with the existing annotations form the QFace document.

.. warning:: External annotation with the same name will override the QFace document annotation with the same name on the specified symbol.



