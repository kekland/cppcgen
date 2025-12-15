from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from ..model import c, cpp

_primitive_mapping: dict[str, str] = {
  'bool': 'bool',
  'int': 'int',
  'double': 'double',
  'float': 'double',
  'void': 'void',
  'char': 'int',
}

_primitive_ffi_mapping: dict[str, str] = {
  'bool': 'ffi.Bool',
  'int': 'ffi.Int',
  'double': 'ffi.Double',
  'float': 'ffi.Float',
  'void': 'ffi.Void',
  'char': 'ffi.Char',
}


@dataclass
# Represents a Dart type. Can be instantiated from a C++ ffi type.
class Type:
  name: str
  nullable: bool = field(default=False)
  cpp_type: Optional[cpp.Type] = field(default=None)

  @staticmethod
  def from_cpp(cpp_type: cpp.Type) -> Type:
    type = cpp_type
    nullable = False

    if type.is_std_optional:
      type = type.unwrapped
      nullable = True

    if type.is_primitive:
      if type.is_pointer: name = _primitive_ffi_mapping.get(type.base_name, 'UNKNOWN')
      else: name = _primitive_mapping.get(type.base_name, 'UNKNOWN')
    elif type.is_decl_enum: name = f'gen_ffi.{type.as_enum.as_c.name}'
    elif type.is_decl_structure: name = f'gen_ffi.{type.as_structure.as_c.name}'
    else: name = 'UNKNOWN'

    if type.is_pointer: name = f'ffi.Pointer<{name}>'
    if nullable: name = f'{name}?'

    return Type(name=name, nullable=nullable, cpp_type=cpp_type)

  @property
  def as_dart(self) -> Type:
    from . import converter
    return converter.convert_type_to_dart(self)


@dataclass
# Represents a Dart enum corresponding to a C++ enum (through C bindings).
class Enum:
  cpp_enum: cpp.Enum

  @property
  def c_enum(self) -> c.Enum: return self.cpp_enum.as_c

  @property
  def name(self) -> str: return self.cpp_enum.name

  @property
  def values(self) -> dict[str, int]: return {value.name: value.value for value in self.cpp_enum.values}

  def generate(self) -> list[str]:
    from .generator import generate_enum
    return generate_enum(self)


@dataclass
# Represents a Dart class corresponding to a C++ structure/class (through C bindings).
class Class:
  cpp_structure: cpp.Structure

  @property
  def c_structure(self) -> c.Structure: return self.cpp_structure.as_c

  @property
  def name(self) -> str: return self.cpp_structure.name

  @property
  def ext_methods(self) -> list[Method]:
    result: list[Method] = []

    for method in self.c_structure.methods:
      m = Method.from_cpp(method).without_instance_param()
      m.impl = [f'return {m.generate_ext_call()};']
      result.append(m)

    return result

  @property
  def ext_fields(self) -> dict[str, tuple[Optional[Method], Optional[Method]]]:
    result: dict[str, tuple[Optional[Method], Optional[Method]]] = {}
    for name in self.c_structure.field_methods:
      getter, setter = self.c_structure.field_methods[name]
      get_m = None
      set_m = None
      if getter:
        m = Method.from_cpp(getter, is_getter=True, name_=name).without_instance_param()
        m.impl = [f'return {m.generate_ext_call()};']
        get_m = m
      if setter:
        m = Method.from_cpp(setter, is_setter=True, name_=name).without_instance_param()
        m.impl = [f'{m.generate_ext_call()};']
        set_m = m
      result[name] = (get_m, set_m)

    return result

  @property
  def methods(self) -> list[Method]:
    from . import converter
    result: list[Method] = []
    for method in self.ext_methods:
      m = method.as_dart
      impl: list[str] = []
      impl.extend(converter.generate_parameters_cast_block(method.parameters))
      impl.append(f'')
      impl.append(f'final result__ = ptr.unwrap().{method.generate_call(param_suffix="_")};')
      impl.append(f'return {converter.generate_cast_from_ffi(method.return_type, "result__")};')
      m.impl = impl
      result.append(m)

    return result

  def generate(self) -> list[str]:
    from .generator import generate_class
    return generate_class(self)


@dataclass
# Represents a Dart method parameter.
class Parameter:
  type: Type
  name: str

  @staticmethod
  def from_cpp(p: cpp.Parameter) -> Parameter: return Parameter(Type.from_cpp(p.type), p.name)

  @property
  def as_dart(self) -> Parameter:
    from . import converter
    return converter.convert_parameter_to_dart(self)


@dataclass
# Represents a Dart method corresponding to a C++ method (through C bindings).
class Method:
  return_type: Type = field()
  name: str = field()
  impl: Optional[list[str]] = field(default=None)
  parameters: list[Parameter] = field(default_factory=list)
  is_getter: bool = field(default=False)
  is_setter: bool = field(default=False)
  is_static: bool = field(default=False)
  cpp_method: Optional[cpp.Method] = field(default=None)

  @staticmethod
  def from_cpp(cpp_method: cpp.Method, is_getter: bool = False, is_setter: bool = False, name_: Optional[str] = None) -> Method:
    parameters = [Parameter.from_cpp(param) for param in cpp_method.parameters]
    name = cpp_method.unprefixed_name
    if cpp_method.base is not None: name = cpp_method.base.unprefixed_name
    if name_ is not None: name = name_

    return Method(
      return_type=Type.from_cpp(cpp_method.return_type),
      name=name,
      parameters=parameters,
      is_getter=is_getter,
      is_setter=is_setter,
      cpp_method=cpp_method,
    )

  @property
  def as_dart(self) -> Method:
    from . import converter
    return converter.convert_method_to_dart(self)

  def without_instance_param(self) -> Method:
    parameters = self.parameters.copy()
    parameters.pop(0)  # Remove instance param
    return Method(
      return_type=self.return_type,
      name=self.name,
      impl=self.impl,
      parameters=parameters,
      is_getter=self.is_getter,
      is_setter=self.is_setter,
      cpp_method=self.cpp_method,
    )

  def generate_ext_call(self) -> str:
    assert self.cpp_method is not None
    call = self.cpp_method.generate_call(param_suffix='')
    call = call.replace('instance', 'this')
    return f'gen_ffi.{call}'

  def generate_signature(self) -> str:
    from .generator import generate_method_signature
    return generate_method_signature(self)

  def generate_decl(self) -> list[str]:
    from .generator import generate_method_decl
    return generate_method_decl(self)

  def generate_impl(self, impl: Optional[list[str]] = None) -> list[str]:
    from .generator import generate_method_impl
    return generate_method_impl(self, impl)

  def generate_call(self, param_suffix: str = '') -> str:
    params = ', '.join([f'{param.name}{param_suffix}' for param in self.parameters])
    return f'{self.name}({params})'
