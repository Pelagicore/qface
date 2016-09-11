# Copyright (c) Pelagicore AG 2016
from collections import OrderedDict, ChainMap
import logging

log = logging.getLogger(__name__)

# System
# +- Module
#   +- Import
#   +- Interface
#     +- Property
#     +- Operation => Method
#   +- Struct (has attributes)
#   +- Enum (has values)


class System(object):
    """The root entity which consist of modules"""
    def __init__(self):
        log.debug('System()')
        self.moduleMap = OrderedDict()  # type: dict[str, Module]

    def __unicode__(self):
        return 'system'

    def __repr__(self):
        return '<System>'

    @property
    def modules(self):
        return self.moduleMap.values()

    def lookup_module(self, name: str):
        return self.moduleMap[name]

    def lookup_interface(self, name: str):
        module_name, type_name = name.rsplit('.', 1)
        module = self.moduleMap[module_name]
        return module.interfaceMap[type_name]

    def lookup_struct(self, name: str):
        module_name, type_name = name.rsplit('.', 1)
        module = self.moduleMap[module_name]
        return module.structMap[type_name]

    def lookup_enum(self, name: str):
        module_name, type_name = name.rsplit('.', 1)
        module = self.moduleMap[module_name]
        return module.enumMap[type_name]

    def lookup_definition(self, name: str):
        # import ipdb; ipdb.set_trace()
        parts = name.rsplit('.', 1)
        if len(parts) == 2:
            module_name = parts[0]
            type_name = parts[1]
            module = self.moduleMap[module_name]
            return module.lookup_definition(type_name)

    @property
    def system(self):
        return self


class Module(object):
    """A module is a namespace for types, e.g. interfaces, enums, structs"""
    def __init__(self, name: str, system: System):
        log.debug('Module()')
        self.name = name
        self.system = system
        self.system.moduleMap[name] = self
        self.interfaceMap = OrderedDict()  # type: dict[str, Interface]
        self.structMap = OrderedDict()  # type: dict[str, Struct]
        self.enumMap = OrderedDict()  # type: dict[str, Enum]
        self.definitionMap = ChainMap(self.interfaceMap, self.structMap, self.enumMap)
        self.importMap = OrderedDict()  # type: dict[str, Module]

    @property
    def interfaces(self):
        return self.interfaceMap.values()

    @property
    def structs(self):
        return self.structMap.values()

    @property
    def enums(self):
        return self.enumMap.values()

    @property
    def imports(self):
        return self.importMap.values()

    @property
    def nameParts(self):
        return self.name.split('.')

    def lookup_definition(self, name: str):
        if name in self.definitionMap:
            return self.definitionMap[name]
        return self.system.lookup_definition(name)

    def lookup_module(self, name: str):
        if name in self.system.moduleMap:
            return self.system.moduleMap[name]

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<{0} name={1}>'.format(type(self), self.name)

    def __str__(self):
        return self.name



class Symbol(object):
    """A symbol represents a base class for names elements"""
    def __init__(self, name: str, module: Module):
        self.name = name
        self.module = module
        self.comment = ''

    @property
    def system(self):
        return self.module.system

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{0} name={1}>'.format(type(self), self.name)

    @property
    def qualifiedName(self):
        return '{0}.{1}'.format(self.module.name, self.name)


class TypedSymbol(Symbol):
    """A symbol which has a type"""
    def __init__(self, name: str, module: Module):
        super().__init__(name, module)
        self.type = TypeSymbol("", self)


class TypeSymbol(Symbol):
    """Defines a type in the system"""
    def __init__(self, name: str, parent: Symbol):
        super().__init__(name, parent.module)
        log.debug('TypeSymbol()')
        self.parent = parent
        self.is_void = False  # type:bool
        self.is_primitive = False  # type:bool
        self.is_complex = False  # type:bool
        self.is_list = False  # type:bool
        self.is_model = False  # type:bool
        self.nested = None
        self.__reference = None
        self.__is_resolved = False

    @property
    def is_bool(self):
        return self.is_primitive and self.name == 'bool'

    @property
    def is_int(self):
        return self.is_primitive and self.name == 'int'

    @property
    def is_real(self):
        return self.is_primitive and self.name == 'real'

    @property
    def is_string(self):
        return self.is_primitive and self.name == 'string'

    @property
    def definition(self):
        if not self.is_complex:
            return
        result = self.module.lookup_definition(self.name)
        if not result:
            result = self.system.lookup_definition(self.name)
        return result

    @property
    def is_enum(self):
        return self.is_complex and isinstance(self.definition, Enum)

    @property
    def is_struct(self):
        return self.is_complex and isinstance(self.definition, Struct)

    @property
    def reference(self):
        """returns the symbol reference of the type name"""
        if not self.__is_resolved:
            self.resolve()
        return self.__reference

    def resolve(self):
        """resolve the type symbol from name by doing a lookup"""
        self.__is_resolved = True
        if self.is_complex:
            type = self.nested if self.nested else self
            type.__reference = self.module.lookup_definition(type.name)



class Interface(Symbol):
    """A interface is an object with operations, properties and events"""
    def __init__(self, name: str, module: Module):
        super().__init__(name, module)
        log.debug('Interface()')
        self.module.interfaceMap[name] = self
        self.propertyMap = OrderedDict()  # type: dict[str, Property]
        self.operationMap = OrderedDict()  # type: dict[str, Operation]
        self.eventMap = OrderedDict()  # type: dict[str, Operation]

    @property
    def properties(self):
        return self.propertyMap.values()

    @property
    def operations(self):
        return self.operationMap.values()

    @property
    def events(self):
        return self.eventMap.values()


class Struct(Symbol):
    """Represents a data container"""
    def __init__(self, name: str, module: Module):
        super().__init__(name, module)
        log.debug('Struct()')
        self.module.structMap[name] = self
        self.memberMap = OrderedDict()  # type: dict[str, Member]

    @property
    def members(self):
        return self.memberMap.values()


class Member(TypedSymbol):
    """A member in a struct"""
    def __init__(self, name: str, struct: Struct):
        super().__init__(name, struct.module)
        log.debug('Member()')
        self.struct = struct  # type:Struct
        self.struct.memberMap[name] = self


class Operation(TypedSymbol):
    """An operation inside a interface"""
    def __init__(self, name: str, interface: Interface, is_event=False):
        super().__init__(name, interface.module)
        log.debug('Operation()')
        self.interface = interface
        self.is_event = is_event
        if is_event:
            self.interface.eventMap[name] = self
        else:
            self.interface.operationMap[name] = self
        self.parameterMap = OrderedDict()  # type: dict[Parameter]

    @property
    def parameters(self):
        return self.parameterMap.values()


class Property(TypedSymbol):
    """A typed property inside a interface"""
    def __init__(self, name: str, interface: Interface):
        super().__init__(name, interface.module)
        log.debug('Property()')
        self.interface = interface
        self.interface.propertyMap[name] = self
        self.is_readonly = False


class Enum(Symbol):
    """An enum (flag) inside a module"""
    def __init__(self, name: str, module: Module):
        super().__init__(name, module)
        log.debug('Enum()')
        self.is_enum = True
        self.is_flag = False
        self.module.enumMap[name] = self
        self.memberMap = OrderedDict()  # type: dict[EnumMember]

    @property
    def members(self):
        return self.memberMap.values()


class EnumMember(Symbol):
    """A enum value"""
    def __init__(self, name: str, enum: Enum):
        super().__init__(name, enum.module)
        log.debug('EnumMember()')
        self.enum = enum
        self.enum.memberMap[name] = self
        self.value = 0


class Parameter(TypedSymbol):
    """An operation parameter"""
    def __init__(self, name: str, operation: Operation):
        super().__init__(name, operation.module)
        log.debug('Parameter()')
        self.operation = operation
        self.operation.parameterMap[name] = self
