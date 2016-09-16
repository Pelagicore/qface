# QML Interface Builder

Infrastructure to build a QML/Qt CPP interface based on an interface definition 
language and templates.

This tool set is not build for highest performance. Rather flexibility in the 
IDL design and generator creation was the goal. It uses great libraries to 
minimize the amount of code required to be maintained.

The code parsing and generation part a very flexible and allows many users to
generate their vision of a QMLCPP interface. 

The Domain language is surely not limited to this.

Please see the INSTALL and USAGE guides for more information.

## Echo Example

```js
// echo.qdl
module org.example 1.0;

/**!
The echo interface to call someone
on the other side
*/
interface Echo {
    readonly Message lastMessage;
    void echo(Message message);
    event void callMe();
};

struct Message {
    string text;
};
```

Now calling the generator to generate the C++ code.

    qface --generator qtcpp --input echo.qdl --output out

It generates a .PRI file and all code required to regsiter the objects to the qml engine. 
The generated code expects the user implements a generated interface.
