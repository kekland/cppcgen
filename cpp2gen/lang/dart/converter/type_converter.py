from __future__ import annotations

from typing import Optional

from ....builtins import BuiltinStructure
from ....model import Type, Enum, Structure

_primitive_mapping: dict[str, str] = {
  'bool': 'bool',
  'int': 'int',
  'double': 'double',
  'float': 'double',
  'void': 'void',
  'char': 'int',
  'uint8_t': 'int',
  'uint16_t': 'int',
  'uint32_t': 'int',
  'uint64_t': 'int',
  'int8_t': 'int',
  'int16_t': 'int',
  'int32_t': 'int',
  'int64_t': 'int',
}

_ffi_primitive_mapping: dict[str, str] = {
  'bool': 'ffi.Bool',
  'int': 'ffi.Int',
  'double': 'ffi.Double',
  'float': 'ffi.Float',
  'void': 'ffi.Void',
  'char': 'ffi.Char',
  'uint8_t': 'ffi.Uint8',
  'uint16_t': 'ffi.Uint16',
  'uint32_t': 'ffi.Uint32',
  'uint64_t': 'ffi.Uint64',
  'int8_t': 'ffi.Int8',
  'int16_t': 'ffi.Int16',
  'int32_t': 'ffi.Int32',
  'int64_t': 'ffi.Int64',
}


def convert_type_to_ffi_ref_ptr(type: Type) -> Type:
  from ...c import converter as c_converter
  _type = c_converter.convert_type_to_ref_ptr(type)

  if _type.base_name in _primitive_mapping:
    name = _primitive_mapping[_type.base_name]
    if _type.is_pointer: name = _ffi_primitive_mapping[_type.base_name]
    return Type(base_name=name, is_pointer=_type.is_pointer)

  return _type


def convert_type_to_ffi_ptr(type: Type) -> Type:
  from ...c import converter as c_converter
  _type = c_converter.convert_type_to_ptr(type)

  if _type.base_name in _primitive_mapping:
    name = _primitive_mapping[_type.base_name]
    if _type.is_pointer: name = _ffi_primitive_mapping[_type.base_name]
    return Type(base_name=name, is_pointer=_type.is_pointer)

  return _type


def convert_type_to_dart(type: Type) -> Type:
  from ...c import converter as c_converter
  _type = c_converter.convert_type_to_ptr(type)

  if _type.base_name in _primitive_mapping:
    name = _primitive_mapping[_type.base_name]
    if _type.is_pointer: name = _ffi_primitive_mapping[_type.base_name]
    return Type(base_name=name, is_pointer=_type.is_pointer)

  from .enum_converter import convert_enum
  from .structure_converter import convert_structure

  # Convert built-in structures
  from ..builtins import maybe_convert_type_to_builtin
  if builtin := maybe_convert_type_to_builtin(type): return builtin

  if isinstance(type.decl_repr, Enum): return convert_enum(type.decl_repr).type
  if isinstance(type.decl_repr, Structure): return convert_structure(type.decl_repr).type_ptr

  return _type


def _internal_cast_type_to_dart(type: Type, var_name: str, ref_copy=False) -> str:
  if type.is_dart: return var_name
  from . import convert_enum, convert_structure

  if isinstance(type.decl_repr, Enum):
    e = convert_enum(type.decl_repr)
    return f'{e.name}.{e.from_ffi_method.name}({var_name})'
  elif isinstance(type.decl_repr, BuiltinStructure):
    if type.decl_repr.passthrough_type: return _internal_cast_type_to_dart(type.decl_repr.passthrough_type, var_name)
    return f'{var_name}.toDart()'
  elif isinstance(type.decl_repr, Structure):
    s = convert_structure(type.decl_repr)
    if ref_copy: return f'{s.name}.fromFfi({var_name}.copy())'
    return f'{s.name}.fromFfi({var_name})'

  return var_name


def _internal_cast_type_to_ffi(type: Type, var_name: str) -> str:
  if type.is_dart: return var_name

  from . import convert_enum, convert_structure

  if isinstance(type.decl_repr, Enum):
    e = convert_enum(type.decl_repr)
    return f'{var_name}.toFfi()'
  elif isinstance(type.decl_repr, BuiltinStructure):
    if type.decl_repr.passthrough_type: return _internal_cast_type_to_ffi(type.decl_repr.passthrough_type, var_name)
    return f'{var_name}.toFfiPtr(arena: arena)'
  elif isinstance(type.decl_repr, Structure):
    s = convert_structure(type.decl_repr)
    return f'{var_name}.ptr.unwrap()'

  return var_name
