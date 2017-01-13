================
Qt CPP Generator
================

QFace comes with a built in generator called `qtcpp`. It takes qface interface
files and generates Qt CPP as a QML plugin which can be directly used inside
your Qt5 project.

The structs/enums/flags are defined in an own module singleton which acts as a namespace and factory methods.

Each interface is generated into a QObject with the defined properties, signals and operations.

For example an QFace document like this

.. code-block:: js

    module sample 1.0

    interface Heater {
        real temperature;
        Status status;
        void increaseTemperature(real step);
        void decreaseTemperature(real step);
        event void error(string message);
    }

    enum Status {
        Null,
        Ready,
        Error
    }


The QTCPP generator will generate all CPP code including the plugin code and project files. Additional it will generate an empty simulation stub.

In QML you would now be able to write the following code.

.. code-block:: qml

    import sample 1.0

    Item {
        Heater {
            id: heater
            onStatusChanged: {
                if(status === SampleModule.Ready) {
                    console.log('ready ...')
                }
            }
            onError: console.log(message)
        }
        Text {
            anchors.centerIn: parent
            text: heater.temperature
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                heater.increaseTemperature(0.5)
            }
        }
    }


Code Generation
===============


For each module the generator creates the qmake project files, the plugin code to register the types. A module singleton which contains the enums and factory functions for creating the structures. The structure has no signals and the values are copied over.

.. code-block:: yml

    for each module:
        - qmldir
        - plugin.h - preserve
        - plugin.cpp - preserve
        - plugin.pro - preserve
        - private/module.h
        - private/module.cpp
        - for each interface:
            - private/abstractinterface.h
            - private/abstractinterface.cpp 
            - interface.h - preserve
            - interface.cpp - preserve
        - for each struct:
            - private/struct.h
            - private/struct.cpp

An base implementation of the interface is generated in the private folder. A stub implementation derived form the abstract interface is generated and registered with the plugin.

Each structure is generates as a Q_GADGET which behaves similar as a JS object on the QML side. The interface is by default registered as a normal QML type and contains the properties and methods as also signals as defined in the interface files.

Design Decisions
================

* All properties generated are read only from QML

    Writable properties on service objects are a cause of errors and confusion. It is very easy in the HMI stack to overwrite a binding property which writes to a service. It is better to offer a dedicated operation which does some work and triggers an operation update.

* All models generated are read only from QML
  
    The data for a model is often stored inside another system (SQL DB, Remote, File System) and only a small subset of the data is actually in memory. Filtering, sorting or modifying the model data should be explicitly done using operations if supported by the user interface.

* Data structures are exported as gadgets
  
    A Q_GADGET allows us to define a data structure and modify its contents. A gadget does not support signals, which means others are not notified about changes. This is the same behavior as for JS objects. Gadgets are copied from C++ to QML so there is no issue with memory management. QML has no means to create a gadget class, for this the module object contains a factory method for each structure.

* Enums are collected into one module object

    All enumerations are defined inside the module object. This allows us to remove the need to additional QObjects per enum. It has the drawback that each enum value should be unique in the module. The generator currently does not enforces this.


Extending the Implementation
============================

To extend the implementation the user needs to modify the interface implementation. The document is marked as preserved, which means it will not re-generated when it exists. To trigger a regeneration the target document needs to be removed.

In the interface document you are able to overwrite all setters and getters as also the operation methods. This is normally the only file you want to modify.

Besides the interface files also the plugin and project files are preserved, as it is expected that these files might be required to change. This may change in the future.




 
