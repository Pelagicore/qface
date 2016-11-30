# QDL grammar

QDL (Qt definnition language) is an IDL to define an interface. In general it is modeled to define an interface between Qt QML and C++. The QDL syntax is flexible enough also to be used in other context.

```html
module <module> <version>
import <module> <version>

interface <Identifier> {
    <type> <identifier>
    <type> <operation>(<parameter>*)
    event <type> <event>(<parameter>*)
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
```

A QDL document always describes one module. Each document can contain one or more interfaces, structs, flags or enums. Each document can import other modules using the import statement.


## Module

A module is identified name. A module should be normally a URI where all parts are lowercase (e.g. `entertainment.tuner`). A module can import other modules. This is used to ensure that dependencies are declared inside the QDL file. 

## Types

Types are either local and can be references simply by its name, or they are from external module in this case they need to be referenced with the fully qualified name (`module + '.' + name`). A type can be an interface, struct, enum or flag.

A module consist of either one or more interfaces, structs and enums/flags. They can come in any number or combination. The interface is the only type which can contain operations and events. The struct is merely a container to transport structured data. An enum/flag allows the user to encode information used inside the struct or interface as datatype.

The QDL does not allow to extend interfaces. It is by design kept simple.

Below is an example of a QDL file.

```java
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
```





