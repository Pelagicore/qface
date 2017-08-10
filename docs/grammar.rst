=======
Grammar
=======

QFace (Qt interface language) is an Interface Description Language (IDL). While it is primarily designed to define an interface between Qt, QML and C++, it is intended to be flexible enough also to be used in other contexts.

The grammar of QFace is well defined and is based on the concepts of modules as larger collection of information.

A module can have several interfaces, structs and/or enums/flags.

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

.. code-block:: js

    // org.example.qface
    module org.example 1.0

    import org.common 1.0


Interface
=========

An interface is a collection of properties, operation and signals. Properties carry data, whereas the operations normally modify the data. Signals are used to notify the user of changes.

.. code-block:: js

    interface WeatherStation {
        real temperature;
        void reset();
        signal error(string message);
    }

QFace allows to extends interfaces using the ``extends`` keyword after the interface name.

.. code-block:: js

    interface Station {
        void reset();
        signal error(string message);
    }

    interface WeatherStation extends Station {
        real temperature;
    }

.. note::

    For the sake of simplicity as an API designer you should carefully evaluate if this is required. The typical way in QFace to allow extension is normally to write your own code-generator and use type annotations.


    .. code-block:: js

        @station
        interface WeatherStation {
            real temperature;
        }

    The API reader does not need to know the internals of the API. The station behavior would be automatically attached by the custom generator.



Struct
======

The struct resembles a data container. It consist of a set of fields where each field has a data type and a name.

.. code-block:: js

    struct Error {
        string message;
        int code;
    };

Structs can also be nested. A struct can be used everywhere where a type can be used.

.. code-block:: js

    interface WeatherStation {
        real temperature;
        Error lastError;
        void reset();
        signal error(Error error);
    }



Enum/Flag
=========

An enum and flag is an enumeration type. The value of each member is automatically assigned if missing.

.. code-block:: js

    enum State {
        Null,
        Loading,
        Ready,
        Error
    }

The value assignment for the enum type is sequential beginning from 0. To specify the exact value you can assign a value to the member.

.. code-block:: js

    enum State {
        Null = 0,
        Loading = 1,
        Ready = 2,
        Error = 3
    }

The flag type defines an enumeration type where these different values are treated as a bit mask. The values are in the sequence of the 2^n.

.. code-block:: js

    flag Cell {
        Null,
        Box,
        Wall,
        Figure
    }



Types
=====

Types are either local and can be references simply by its name, or they are from external module in this case they need to be referenced with the fully qualified name (``<module>.<symbol>``). A type can be an interface, struct, enum or flag. It is also possible to reference the inner members of the symbols with the fragment syntax (``<module>.<symbol>#<fragment>``).

A module consist of either one or more interfaces, structs and enums/flags. They can come in any number or combination. The interface is the only type which can contain properties, operations and signals. The struct is merely a container to transport structured data. An enum/flag allows the user to encode information used inside the struct or interface as data-type.

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


Annotations
===========

Annotation allow the writer to add meta data to an interface document. It uses the `@` notation followed by valid YAML one line content.

.. code-block:: js

    @singleton: true
    @config: { port: 1234 }
    interface Echo {
    }

More information on annotations can be found in the annotations chapter.

Comments
========

Comments use the JavaDoc convention of using an `@` sign as prefix with the keyword followed by the required parameters.

.. code-block::java

    /**
     * @brief The last echo message
     */

Currently only brief, description, see and deprecated are supported doc tags.

The QtCPP built-in generator generates valid Qt documentation out of these comments.


