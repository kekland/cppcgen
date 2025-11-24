from __future__ import annotations

from ...model import cpp


def generate_type(type: cpp.Type) -> str:
  return type.full_name


def generate_type_cast_to_c_ref(type: cpp.Type, var_name: str) -> str:
  if type.is_c_type: return var_name

  if type.is_decl_enum:
    e = type.as_enum
    return f'{e.to_c_fn.full_name}({var_name})'
  elif type.is_decl_structure:
    s = type.as_structure
    s_c = s.as_c
    return f'{s_c.wrap_ref_type(var_name)}'

  return var_name


def generate_type_cast_to_c_ptr(type: cpp.Type, var_name: str) -> str:
  if type.is_c_type: return var_name

  if type.is_decl_enum:
    e = type.as_enum
    return f'{e.to_c_fn.full_name}({var_name})'
  elif type.is_decl_structure:
    s = type.as_structure
    s_c = s.as_c
    return f'{s_c.wrap_type(var_name)}'

  return var_name


def generate_type_cast_to_cpp(type: cpp.Type, var_name: str) -> str:
  if type.is_decl_enum:
    e = type.as_enum
    return f'{e.from_c_fn.full_name}({var_name})'
  elif type.is_decl_structure:
    s = type.as_structure
    s_c = s.as_c
    return f'*{s_c.unwrap_type(var_name)}'

  return var_name
