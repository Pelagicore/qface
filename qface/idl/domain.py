# Copyright (c) Pelagicore AB 2016

'''The domian module contains an object hierachy which resembles the
QFace grammar as a domain model. It is created from the QFace and the main
input for the code generation templates.

.. note:: Changes on this API will result into broken templates

.. code-block:: text

    System
     +- Module
       +- Import
       +- Interface
         +- Property
         +- Operation
         +- Event
       +- Struct (has attributes)
       +- Enum (has values)

.. note::

    When the API talks about an order list, the order is by appearance
    in the QFace file.
'''

from collections import OrderedDict, ChainMap
import click
import logging

log = logging.getLogger(__name__)


class System(object):
    """The root entity which consist of modules"""
    def __init__(self):
        log.debug('System()')
        self._moduleMap = OrderedDict()  # type: dict[str, Module]

    def __unicode__(self):
        return 'system'

    def __repr__(self):
        return '<System>'

    @property
    def modules(self):
        '''returns ordered list of module symbols'''
        return self._moduleMap.values()

    def lookup(self, name: str):
        '''lookup a symbol by fully qualified name.'''
        # <module>
        if name in self._moduleMap:
            return self._moduleMap[name]
        # <module>.<Symbol>
        (module_name, type_name, fragment_name) = self.split_typename(name)
        if not module_name and type_name:
            click.secho('not able to lookup symbol: {0}'.format(name), fg='red')
            return None
        module = self._moduleMap[module_name]
        return module.lookup(type_name, fragment_name)

    @staticmethod
    def split_typename(name):
        parts = name.rsplit('#', 1)
        fragment_name = None
        module_name = None
        type_name = None
        if len(parts) == 2:
            fragment_name = parts[1]
        name = parts[0]
        parts = name.rsplit('.', 1)
        if len(parts) == 1:
            type_name = parts[0]
        elif len(parts) == 2:
            module_name = parts[0]
            type_name = parts[1]
        return (module_name, type_name, fragment_name)


class NamedElement(object):
    def __init__(self, name, module: 'Module'):
        self.name = name
        """symbol name"""
        self.module = module
        """module the symbol belongs to"""

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{0} name={1}>'.format(type(self), self.name)

    @property
    def qualified_name(self):
        '''return the fully qualified name (`module + "." + name`)'''
        if self.module == self:
            return self.module.name
        else:
            return '{0}.{1}'.format(self.module.name, self.name)


class Symbol(NamedElement):
    """A symbol represents a base class for names elements"""
    def __init__(self, name: str, module: 'Module'):
        super().__init__(name, module)
        self.comment = ''
        """comment which appeared in QFace right before symbol"""
        self._tags = OrderedDict()

        self._contentMap = ChainMap()
        self.type = TypeSymbol('', self)

    @property
    def system(self):
        '''returns reference to system'''
        return self.module._system

    @property
    def tags(self):
        return self._tags

    def add_tag(self, tag):
        if tag not in self._tags:
            self._tags[tag] = OrderedDict()

    def add_attribute(self, tag, name, value):
        self.add_tag(tag)
        d = self._tags[tag]
        d[name] = value

    def tag(self, name):
        return self._tags[name]

    def attribute(self, tag, name):
        if tag in self._tags:
            return self._tags[tag][name]

    @property
    def contents(self):
        return self._contentMap.values()



class TypeSymbol(NamedElement):
    """Defines a type in the system"""
    def __init__(self, name: str, parent: NamedElement):
        super().__init__(name, parent.module)
        log.debug('TypeSymbol()')
        self.parent = parent
        self.is_void = False  # type:bool
        self.is_primitive = False  # type:bool
        self.is_complex = False  # type:bool
        self.is_list = False  # type:bool
        self.is_model = False  # type:bool
        self.nested = None
        """nested type if symbol is list or model"""
        self.__reference = None
        self.__is_resolved = False

    @property
    def is_valid(self):
        '''checks if type is a valid type'''
        return self.is_primitive or self.is_complex

    @property
    def is_bool(self):
        '''checks if type is primitive and bool'''
        return self.is_primitive and self.name == 'bool'

    @property
    def is_int(self):
        '''checks if type is primitive and int'''
        return self.is_primitive and self.name == 'int'

    @property
    def is_real(self):
        '''checks if type is primitive and real'''
        return self.is_primitive and self.name == 'real'

    @property
    def is_string(self):
        '''checks if type is primitive and string'''
        return self.is_primitive and self.name == 'string'

    @property
    def is_enum(self):
        '''checks if type is complex and enum'''
        return self.is_complex and isinstance(self.reference, Enum)

    @property
    def is_struct(self):
        '''checks if type is complex and struct'''
        return self.is_complex and isinstance(self.reference, Struct)

    @property
    def is_variant(self):
        '''checks if type is primitive and string'''
        return self.is_primitive and self.name == 'var'

    @property
    def reference(self):
        """returns the symbol reference of the type name"""
        if not self.__is_resolved:
            self._resolve()
        return self.__reference

    def _resolve(self):
        """resolve the type symbol from name by doing a lookup"""
        self.__is_resolved = True
        if self.is_complex:
            type = self.nested if self.nested else self
            type.__reference = self.module.lookup(type.name)

    @property
    def type(self):
        return self


class Module(Symbol):
    """Module is a namespace for types, e.g. interfaces, enums, structs"""
    def __init__(self, name: str, system: System):
        """init"""
        super().__init__(name, self)
        log.debug('Module()')
        self.version = '1.0'
        self._system = system
        self._system._moduleMap[name] = self
        self._interfaceMap = OrderedDict()  # type: dict[str, Interface]
        self._structMap = OrderedDict()  # type: dict[str, Struct]
        self._enumMap = OrderedDict()  # type: dict[str, Enum]
        self._contentMap = ChainMap(self._interfaceMap, self._structMap, self._enumMap)
        self._importMap = OrderedDict()  # type: dict[str, Module]

    @property
    def interfaces(self):
        '''returns ordered list of interface symbols'''
        return self._interfaceMap.values()

    @property
    def structs(self):
        '''returns ordered list of struct symbols'''
        return self._structMap.values()

    @property
    def enums(self):
        '''returns ordered list of enum symbols'''
        return self._enumMap.values()

    @property
    def imports(self):
        '''returns ordered list of import symbols'''
        return self._importMap.values()

    def checkType(self, type: str):
        if type.is_primitive:
            return True
        (module_name, type_name, fragment_name) = System.split_typename(type.name)
        if module_name and module_name not in self._importMap:
            return False
        return True

    @property
    def name_parts(self):
        '''return module name splitted by '.' in parts'''
        return self.name.split('.')

    @property
    def module_name(self):
        return self.name.split('.')[-1].capitalize()

    def lookup(self, name: str, fragment: str = None):
        '''lookup a symbol by name. If symbol is not local
        it will be looked up system wide'''
        if name in self._contentMap:
            symbol = self._contentMap[name]
            if fragment:
                return symbol._contentMap[fragment]
            return symbol
        return self.system.lookup(name)


class Interface(Symbol):
    """A interface is an object with operations, properties and signals"""
    def __init__(self, name: str, module: Module):
        super().__init__(name, module)
        log.debug('Interface()')
        self.module._interfaceMap[name] = self
        self._propertyMap = OrderedDict()  # type: dict[str, Property]
        self._operationMap = OrderedDict()  # type: dict[str, Operation]
        self._signalMap = OrderedDict()  # type: dict[str, Signal]
        self._contentMap = ChainMap(self._propertyMap, self._operationMap, self._signalMap)

    @property
    def properties(self):
        '''returns ordered list of properties'''
        return self._propertyMap.values()

    @property
    def operations(self):
        '''returns ordered list of operations'''
        return self._operationMap.values()

    @property
    def signals(self):
        '''returns ordered list of signals'''
        return self._signalMap.values()


class Operation(Symbol):
    """An operation inside a interface"""
    def __init__(self, name: str, interface: Interface):
        super().__init__(name, interface.module)
        log.debug('Operation()')
        self.interface = interface
        self.interface._operationMap[name] = self
        self._parameterMap = self._contentMap = OrderedDict()  # type: dict[Parameter]

    @property
    def parameters(self):
        '''returns ordered list of parameters'''
        return self._parameterMap.values()


class Signal(Symbol):
    """A signal inside an interface"""
    def __init__(self, name: str, interface: Interface):
        super().__init__(name, interface.module)
        log.debug('Signal()')
        self.interface = interface
        self.interface._signalMap[name] = self
        self._parameterMap = self._contentMap = OrderedDict()  # type: dict[Parameter]

    @property
    def parameters(self):
        '''returns ordered list of parameters'''
        return self._parameterMap.values()


class Parameter(Symbol):
    """An operation parameter"""
    def __init__(self, name: str, operation: Operation):
        super().__init__(name, operation.module)
        log.debug('Parameter()')
        self.operation = operation
        self.operation._parameterMap[name] = self


class Property(Symbol):
    """A typed property inside a interface"""
    def __init__(self, name: str, interface: Interface):
        super().__init__(name, interface.module)
        log.debug('Property()')
        self.interface = interface
        self.interface._propertyMap[name] = self
        self.is_readonly = False


class Struct(Symbol):
    """Represents a data container"""
    def __init__(self, name: str, module: Module):
        super().__init__(name, module)
        log.debug('Struct()')
        self.module._structMap[name] = self
        self._fieldMap = self._contentMap = OrderedDict()  # type: dict[str, Field]

    @property
    def fields(self):
        '''returns ordered list of members'''
        return self._fieldMap.values()


class Field(Symbol):
    """A member in a struct"""
    def __init__(self, name: str, struct: Struct):
        super().__init__(name, struct.module)
        log.debug('Field()')
        self.struct = struct  # type:Struct
        self.struct._fieldMap[name] = self


class Enum(Symbol):
    """An enum (flag) inside a module"""
    def __init__(self, name: str, module: Module):
        super().__init__(name, module)
        log.debug('Enum()')
        self.is_enum = True
        self.is_flag = False
        self.module._enumMap[name] = self
        self._memberMap = self._contentMap = OrderedDict()  # type: dict[EnumMember]

    @property
    def members(self):
        '''returns ordered list of members'''
        return self._memberMap.values()


class EnumMember(Symbol):
    """A enum value"""
    def __init__(self, name: str, enum: Enum):
        super().__init__(name, enum.module)
        log.debug('EnumMember()')
        self.enum = enum
        self.enum._memberMap[name] = self
        self.value = 0
