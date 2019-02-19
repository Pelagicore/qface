**********
Rules Mode
**********

In the rules mode, qface is used as the qface exectuable. In this mode the code generator consits of a rule document and template files and optionally a filter module.

Whereas normally the generator writer create an own python package in this module only some documents are needed and the qface rules is used.

Setup
=====

To get started create a `qface-rules.yml` document and a templates folder::

    qface-rules.yml
    templates/


In the rules file you provide the code generation rules according to the rule generator documentation. The templates folder will contain the required templates.

Filters
=======

To provide extra filder you need to create a `filters.py` document with the declaration of your filters::

    # a filter takes in a domain element or string
    # and returns a string
    def echo(s):
        return '{} World!'.format(s)

    def get_filters():
        # returns a dict of new filters
        return {
            'echo': echo
        }

The filters module will be loaded by qface and all entries to the filters dictionary are added to the global lists of Jinja filters. You can now use it like any other Jinja filter.

.. code-block:: jinja

    {{ "Hello" | echo }}

Will resolve to ``Hello World!``.


Running
=======

To run now the generator you can simply call::

    qface --rules qface-rules.yml --target out counter.qface

This will take your rules and generate the files inside the out folder based on the `counter.qface` interface file.
