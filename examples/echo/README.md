# Echo Example

Allow you to generate the echo QML plugins from the echo interfaces and show how to use them.

## Running the Generator
```sh
../../builtin/qtcpp/qtcpp.py ../interfaces/echo.qface ../plugins
```

## Building the Plugins
Now you can open the plugins.pro file and build the plugins

```sh
qmake
make
make install
```

## Running the Echo App

Now you can build the echo app and use the generated plugins

```sh
cd echo
qmake
make
./echo
```


