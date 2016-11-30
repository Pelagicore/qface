# Builtin Generators

## QtCPP Generator

This is one of the buit-in generators to generate a QtCPP API to be exported into QML. 
The structs/enums/flags are defined in an own Module Qbject which acts as a namespace and can not be instantiated.

Each interface is generated into a QObject with proper properties, signals and invokables.

For example an QDL like this:

```js
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
```

The QTCPP generator will generate all CPP code including the plugin code and project files. Additional it will generate an empy simulation stub.

In QML you would now be able to write the following code.

```qml
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
```