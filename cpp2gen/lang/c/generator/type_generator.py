from __future__ import annotations

from typing import Optional

from ....model import Type, Enum, Structure


def generate_type(type: Type) -> str:
  if type.is_cpp: return type.full_name_cpp_str
  if type.is_c:
    if type.is_pointer:
      if isinstance(type.decl_repr, Enum): return 'int*'
      elif isinstance(type.decl_repr, Structure): return f'{type.decl_repr.name}_t'
      else: return 'void*'

    return type.base_name
  if type.is_dart: raise ValueError('Dart types cannot be generated in C')

  return type.full_name_cpp_str
