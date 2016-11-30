# Installation

Installing as python executable using pip3 (python3)

    git clone git@github.com:Pelagicore/qface.git
    cd qface
    pip3 install -e .

Installs qface as an "editable" package. Means updates on the local git repo are reflected. If this is not what you want you can install it with

    cd qface
    pip3 install .


# Setup Develoment

To install the python dependencies use

    cd qface
    pip3 install -r requirements
    pip3 install -e .

For updating the grammar you also need antlr4 (see http://www.antlr.org).

# Tests

The commands are controlled by the cli.py script.

    cd qface
    ./cli.py --help

To run the tests once

    ./cli.py test

To monitor the tests and auto-run the tests

    cd qface
    ./cli.py test_monitor




