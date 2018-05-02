***********
Annotations
***********

Annotations allow to add meta information to your interface definition. It
is available to each symbol in the interface.

With annotations an interface author can extend the existing interface with additional meta information, called tags, aka annotations. One or several annotations can precede a module, ``interface``, ``struct`` or ``enum``. They are also allowed before an ``operation``, ``property`` or ``signal``. Everywhere where a documentation comment is allowed you can also add annotations.

An annotation looks like this

.. code-block:: python

    @service: {port: 12345}
    interface Tuner {
    }


An embedded annotation precedes a symbol and it starts with an ``@`` sign. A symbol can have more than one annotation line. Each line should be one individual annotation. The content is YAML content. All ``@`` signs preceding a symbol are collected and then evaluated using a YAML parser.

For larger annotations you can use the external annotation document feature (see below).

.. code-block:: python

    @singleton: yes
    @data: [1,2,3]
    @config: { values: [LEFT, RIGHT, TOP] }

This will be result into a YAML content of


.. code-block:: yaml

    singleton: yes
    data: [1,2,3]
    config: { values: [LEFT, RIGHT, TOP] }

And the result as Python object would be

.. code-block:: python

    {
      "data": [ 1, 2, 3 ],
      "singleton": true,
      "config": {
        "values": [ "LEFT", "RIGHT", "TOP" ]
      }
    }

Annotation Documents
====================

QFace allows also to specify these annotations in external documents using the `YAML` syntax. For this you need to create a document with the same name as the QFace document but with the extension `.yaml`. It should have roughly the following format

.. code-block:: yaml

    com.pelagicore.ivi.Tuner:
        service:
            port: 12345

On the root level should be a fully qualified name of a symbol. The symbol will be looked up and the following annotation information merged with the existing annotations from the QFace document.

Merging Annotations
===================

The external annotations will be merged on top of the embedded annotations per symbol. Dictionaries will be merged. If a merge can not be done then the external document based annotations will override the embedded annotations.

Generators
==========

Annotations are available later when navigating the domain model.

.. code-block:: jinja2

    {% if "service" in interface.tags %}
    interface {{interface}} is served on port: {{interface.tags.service.port}}
    {% else %}
    interface {{interface}} is not served
    {% endif %}

.. note:: QFace does not specify specific annotations, but defines just the annotation format. The set of annotations supported must be defined and documented by the generator.






