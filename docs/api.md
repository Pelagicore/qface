# API

The API mostly consist of two helper classes and the domain model. For the domain model, see the domain documentation.

## qface.generator.FileSystem

* FileSystem.parse_document(path: str, system: System = None)
    
    Parses a document and returns the resulting domain system

* FileSystem.parse_dir(path, identifier: str = None, clear_cache=True)
    
    Recursively parses a directory and returns the resulting system

* FileSystem.find_files(path, glob='*.qdl')
    
    Find recursively all files in the given path using the glob parameter

## qface.generator.Generator

* Generator(searchpath)
    
    Manages the templates and applies your context data

* generator.get_template(self, name: str)
    
    Retrievs a single template file from the template loader

* generator.render(self, name: str, context: dict)
    
    Returns the rendered text from a single template file

* generator.apply(self, template: Template, context: dict)
    
    Return the rendered text of a template instance

* generator.write(self, fileTemplate: str, template: str, context: dict)
    
    Using a templated file name it renders a template into a file given a context

* generator.register_filter(self, name, callback)
    
    Register your custom template filter
