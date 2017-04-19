****************
JSON Meta Export
****************

QFace allows you to easily export the domain model as a JSON document. This enables you to parse the domain information to be
used with other tooling.

Inside your generator you need to register the filter first

.. code-block:: python

    from qface.filters import jsonify


    generator = Generator(search_path=search_path)
    generator.register_filter('jsonify', jsonify)

Then inside the template you can transform any symbol into a JSON string using the ``jsonify`` filter.

.. code-block:: jinja

    {{module|jsonify}}

Depending on your need you might want to create a JSON document form the whole system or from each interface or you are just
interested for example on a JSON representation of a enumeration.

JSON Format
===========

Taking the example QFace document

.. code-block:: thrift

    module org.example 1.0;

    interface Echo {
        readonly string currentMessage;
        void echo(Message message);
    }

    struct Message {
        string text;
    }

    enum Status {
        Null,
        Loading,
        Ready,
        Error
    }


The following JSON output is generated

.. code-block:: json

    {
      "name": "org.example",
      "version": "1.0",
      "interfaces": [
        {
          "name": "Echo",
          "properties": [
            {
              "name": "currentMessage",
              "type": {
                "name": "string",
                "primitive": true
              },
              "readonly": true
            }
          ],
          "operations": [
            {
              "name": "echo",
              "parameters": [
                {
                  "name": "message",
                  "type": {
                    "name": "Message",
                    "complex": true
                  }
                }
              ]
            }
          ],
          "signals": []
        }
      ],
      "structs": [
        {
          "name": "Message",
          "fields": [
            {
              "name": "text",
              "type": {
                "name": "string",
                "primitive": true
              }
            }
          ]
        }
      ],
      "enums": [
        {
          "name": "Status",
          "enum": true,
          "members": [
            {
              "name": "Null",
              "value": 0
            },
            {
              "name": "Loading",
              "value": 1
            },
            {
              "name": "Ready",
              "value": 2
            },
            {
              "name": "Error",
              "value": 3
            }
          ]
        }
      ]
    }