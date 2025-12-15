from __future__ import annotations

from typing import Optional

from ....model import Type, Enum, Structure


def _convert_type(type: Type) -> Optional[Type]:
  if type.is_dart: raise ValueError('Cannot convert Dart type to C type')
  if type.is_c: return type

  from .enum_converter import convert_enum
  if isinstance(type.decl_repr, Enum): return convert_enum(type.decl_repr).type
  return None


def convert_type(type: Type) -> Type:
  result = _convert_type(type)
  if result is not None: return result

  from .structure_converter import convert_structure_lite
  if isinstance(type.decl_repr, Structure): return convert_structure_lite(type.decl_repr).type
  return type


def convert_type_to_ref_ptr(type: Type) -> Type:
  result = _convert_type(type)
  if result is not None: return result

  from .structure_converter import convert_structure_lite
  if isinstance(type.decl_repr, Structure): return convert_structure_lite(type.decl_repr).ref.type_ptr
  return type


def convert_type_to_ptr(type: Type) -> Type:
  result = _convert_type(type)
  if result is not None: return result

  from .structure_converter import convert_structure_lite
  if isinstance(type.decl_repr, Structure): return convert_structure_lite(type.decl_repr).type_ptr
  return type


def _internal_cast_type_to_ref_ptr(type: Type, var_name: str) -> str:
  if type.is_dart: raise ValueError('Cannot convert Dart type to C type')
  if type.is_c: return var_name

  from . import convert_enum, convert_structure_lite

  if isinstance(type.decl_repr, Enum):
    e = convert_enum(type.decl_repr)
    return f'enum_cv::{e.to_c_method.name}({var_name})'
  elif isinstance(type.decl_repr, Structure):
    s = convert_structure_lite(type.decl_repr)
    return s.ref.wrap(var_name)

  return var_name


def _internal_cast_type_to_ptr(type: Type, var_name: str) -> str:
  if type.is_dart: raise ValueError('Cannot convert Dart type to C type')
  if type.is_c: return var_name

  from . import convert_enum, convert_structure_lite

  if isinstance(type.decl_repr, Enum):
    e = convert_enum(type.decl_repr)
    return f'enum_cv::{e.to_c_method.name}({var_name})'
  elif isinstance(type.decl_repr, Structure):
    s = convert_structure_lite(type.decl_repr)
    return s.wrap(var_name)

  return var_name


def _internal_cast_type_to_cpp(type: Type, var_name: str) -> str:
  if type.is_dart: raise ValueError('Cannot convert Dart type to C type')
  if type.is_c: return var_name

  from . import convert_enum, convert_structure_lite

  if isinstance(type.decl_repr, Enum):
    e = convert_enum(type.decl_repr)
    return f'enum_cv::{e.from_c_method.name}({var_name})'
  elif isinstance(type.decl_repr, Structure):
    s = convert_structure_lite(type.decl_repr)
    if type.is_pointer: return f'{s.unwrap(var_name)}'
    else: return f'*{s.unwrap(var_name)}'

  return var_name
