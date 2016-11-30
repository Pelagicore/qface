# API

The API mostly consist of two helper classes and the domain model. For the domain model, see the domain documentation.

## qface.generator.FileSystem

* FileSystem.parse_document(path: str, system: System = None)
* FileSystem.parse_dir(path, identifier: str = None, clear_cache=True)
* FileSystem.find_files(path, glob='*.qdl')

## qface.generator.Generator

* Generator(searchpath)
    Manages the templates and applies your context data
* generator.get_template(self, name: str)
    Retrievs a single template file from the template loader
* generator.render(self, name: str, context: dict)
* generator.apply(self, template: Template, context: dict)
* generator.write(self, fileTemplate: str, template: str, context: dict)
* generator.register_filter(self, name, callback)