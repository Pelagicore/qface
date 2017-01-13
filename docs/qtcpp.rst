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
        void increaseTemperature(qreal step);
        void decreaseTemperature(qreal step);
        event void error(string message);
    }

    enum Status {
        Null,
        Ready,
        Error
    }


The QTCPP generator will generate all CPP code including the plugin code and project files. Additional it will generate an empy simulation stub.

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

Each structure is generates as a Q_GADGET which behaves similar as a JS object on the QML side. The interface is by default registered as a normal qml type and contains the properties and methods as also signals as defined in the interface files.

Extending the Implementation
============================

To extend the implementation the user needs to modify the interface implementation. The document is marked as preserved, which means it will not re-generated when it exists. To trigger a regeneration the target document needs to be removed.

In the interface document you are able to overwrite all setters and getters as also the operation methods. This is normally the only file you want to modify.

Besides the interface files also the plugin and project files are preserved, as it is expected that these files might be required to change. This may change in the future.

 
