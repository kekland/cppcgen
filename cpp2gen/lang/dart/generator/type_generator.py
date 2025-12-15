from __future__ import annotations

from typing import Optional

from ....model import Type, Enum, Structure


def generate_type(type: Type) -> str:
  if type.is_cpp: raise ValueError('C++ types cannot be generated in Dart')
  if type.is_c:
    if type.is_pointer:
      if isinstance(type.decl_repr, Enum): return 'ffi.Pointer<ffi.Int>'
      elif isinstance(type.decl_repr, Structure): return f'gen_ffi.{type.base_name}_t'
      else: return 'ffi.Pointer<ffi.Void>'

    return f'gen_ffi.{type.base_name}'

  if type.is_pointer and type.base_name.startswith('ffi.'): return f'ffi.Pointer<{type.base_name}>'

  base = type.base_name

  if type.template_args and len(type.template_args) > 0:
    args = ', '.join([generate_type(arg) if isinstance(arg, Type) else str(arg) for arg in type.template_args])
    base += f'<{args}>'

  return base
