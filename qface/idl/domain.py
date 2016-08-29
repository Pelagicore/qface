from collections import OrderedDict, ChainMap
import logging

log = logging.getLogger(__name__)

# System
# +- Package
#   +- Import
#   +- Service
#     +- Attribute
#     +- Operation
#   +- Struct
#   +- Enum



class System(object):
    def __init__(self):
        log.debug('System()')
        self.packageMap = OrderedDict()  # type: Dict[str, Package]

    def __unicode__(self):
        return 'system'

    def __repr__(self):
        return '<System>'

    @property
    def packages(self):
        return self.packageMap.values()

    def lookup_package(self, name: str):
        return self.packageMap[name]

    def lookup_service(self, name: str):
        package_name, type_name = name.rsplit('.', 1)
        package = self.packageMap[package_name]
        return package.serviceMap[type_name]

    def lookup_struct(self, name: str):
        package_name, type_name = name.rsplit('.', 1)
        package = self.packageMap[package_name]
        return package.structMap[type_name]

    def lookup_enum(self, name: str):
        package_name, type_name = name.rsplit('.', 1)
        package = self.packageMap[package_name]
        return package.enumMap[type_name]

    def lookup_definition(self, name: str):
        parts = name.rsplit('.', 1)
        if len(parts) == 2:
            package_name = parts[0]
            type_name = parts[1]
            package = self.packageMap[package_name]
            return package.lookup_definition(type_name)

    @property
    def system(self):
        return self


class Package(object):
    def __init__(self, name: str, system: System):
        log.debug('Package()')
        self.name = name
        self.system = system
        self.system.packageMap[name] = self
        self.serviceMap = OrderedDict()  # type: Dict[str, Service]
        self.structMap = OrderedDict()  # type: Dict[str, Struct]
        self.enumMap = OrderedDict()  # type: Dict[str, Enum]
        self.definitionMap = ChainMap(self.serviceMap, self.structMap, self.enumMap)
        self.importMap = OrderedDict()  # type: Dict[str, Package]

    @property
    def services(self):
        return self.serviceMap.values()

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

    def lookup_package(self, name: str):
        if name in self.system.packageMap:
            return self.system.packageMap[name]

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name



class Symbol(object):
    def __init__(self, name: str, package: Package):
        self.name = name
        self.package = package
        self.comment = ''

    @property
    def system(self):
        return self.package.system

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def qualifiedName(self):
        return '{0}.{1}'.format(self.package.name, self.name)


class TypedSymbol(Symbol):
    def __init__(self, name: str, package: Package):
        super().__init__(name, package)
        self.type = TypeSymbol("", self)


class TypeSymbol(Symbol):
    def __init__(self, name: str, parent: Symbol):
        super().__init__(name, parent.package)
        log.debug('TypeSymbol()')
        self.parent = parent
        self.is_void = False  # type:bool
        self.is_primitive = False  # type:bool
        self.is_complex = False  # type:bool
        self.is_list = False  # type:bool
        self.is_model = False  # type:bool

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
        result = self.package.lookup_definition(self.name)
        if not result:
            result = self.system.lookup_definition(self.name)
        return result

    @property
    def is_enum(self):
        return self.is_complex and isinstance(self.definition, Enum)

    @property
    def is_struct(self):
        return self.is_complex and isinstance(self.definition, Struct)



class Service(Symbol):
    def __init__(self, name: str, package: Package):
        super().__init__(name, package)
        log.debug('Service()')
        self.package.serviceMap[name] = self
        self.attributeMap = OrderedDict()  # type: Dict[str, Attribute]
        self.operationMap = OrderedDict()  # type: Dict[str, Operation]
        self.eventMap = OrderedDict()  # type: Dict[str, Operation]

    @property
    def attributes(self):
        return self.attributeMap.values()

    @property
    def operations(self):
        return self.operationMap.values()

    @property
    def events(self):
        return self.eventMap.values()


class Struct(Symbol):
    def __init__(self, name: str, package: Package):
        super().__init__(name, package)
        log.debug('Struct()')
        self.package.structMap[name] = self
        self.memberMap = OrderedDict()  # type: Dict[str, Member]

    @property
    def members(self):
        return self.memberMap.values()


class Member(TypedSymbol):
    def __init__(self, name: str, struct: Struct):
        super().__init__(name, struct.package)
        log.debug('Member()')
        self.struct = struct  # type:Struct
        self.struct.memberMap[name] = self


class Operation(TypedSymbol):
    def __init__(self, name: str, service: Service, is_event=False):
        super().__init__(name, service.package)
        log.debug('Operation()')
        self.service = service
        self.is_event = is_event
        if is_event:
            self.service.eventMap[name] = self
        else:
            self.service.operationMap[name] = self
        self.parameterMap = OrderedDict()  # type: Dict[Parameter]

    @property
    def parameters(self):
        return self.parameterMap.values()


class Attribute(TypedSymbol):
    def __init__(self, name: str, service: Service):
        super().__init__(name, service.package)
        log.debug('Attribute()')
        self.service = service
        self.service.attributeMap[name] = self
        self.is_readonly = False


class Enum(Symbol):
    def __init__(self, name: str, package: Package):
        super().__init__(name, package)
        log.debug('Enum()')
        self.is_enum = True
        self.is_flag = False
        self.package.enumMap[name] = self
        self.memberMap = OrderedDict()  # type: Dict[EnumMember]

    @property
    def members(self):
        return self.memberMap.values()


class EnumMember(Symbol):
    def __init__(self, name: str, enum: Enum):
        super().__init__(name, enum.package)
        log.debug('EnumMember()')
        self.enum = enum
        self.enum.memberMap[name] = self
        self.value = 0


class Parameter(TypedSymbol):
    def __init__(self, name: str, operation: Operation):
        super().__init__(name, operation.package)
        log.debug('Parameter()')
        self.operation = operation
        self.operation.parameterMap[name] = self
