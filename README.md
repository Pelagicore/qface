# Qt Interface Builder (QFace)

[![Build Status](https://travis-ci.org/Pelagicore/qface.svg?branch=develop)](https://travis-ci.org/Pelagicore/qface)
[![Documentation Status](https://readthedocs.org/projects/qface/badge/?version=latest)](http://qface.readthedocs.io/en/latest/?badge=latest)

QFace is a generator framework based on a common modern IDL. It is not a generator as such but enforces a common IDL format and provides a library to write your own generator. It is actually very easy to create your own generator and generate your custom solution based on your needs from the same IDL.

The IDL is designed after the Qt/QML interface and as such is optimized to generate source code used with Qt C++ or Qt QML, but it is not limited to this use case.

QFace is already very fast by design and suitable for large IDL document sets. Additionally it can use a cache to avoid parsing unchanged IDL documents. It can automatically avoid writing new files if the target file has the same content.

QFace is written out of the learnings of using IDLs in other large projects. Often in the project you need to adjust the code generation but in many generators this is awfully complicated. Or you need to run a report on the documents or generate specific documentation. In QFace this is enabled by having a very flexible code generation framework which enforces the same IDL.

Please see the INSTALL and USAGE guides for more information.

## Copyright and license

Copyright (C) 2016 Pelagicore AG

The source code in this repository is subject to the terms of the GPLv3 licence, please see included "LICENSE" file for details.


## QFace Example


```js
// echo.qface
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

Now you write a small script using qface to generate your code

```python
# mygenerator.py
from qface.generator import FileSystem, Generator

# load the interface files
system = FileSystem.parse('echo.qface')
# prepare the generator
generator = Generator(searchpath='.')

# iterate over the domain model
for module in system:
    for interface in module:
        # prepare a context object
        ctx = { 'interface': interface }
        # use header.h template with ctx to write to a file
        generator.write('{{interface|lower}}.h', 'header.h', ctx)
``` 

Depending on the used generator it reads the input file and runs it through the generator. The output files are written relative to the given output directory. The input can be either a file or a folder.
