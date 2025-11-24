from __future__ import annotations

from .. import utils
from ..model import cpp
from . import builtins


def cpp_type_to_c_ptr(cpp_type: cpp.Type) -> cpp.Type:
  if cpp_type.is_builtin_structure: return builtins.get_builtin_structure(cpp_type).type
  if cpp_type.is_decl_enum: return cpp_type.as_enum.as_c.type
  if cpp_type.is_decl_structure: return cpp_type.as_structure.as_c.type

  return cpp.Type(
    base_name=utils.cpp_name_to_c_name(cpp_type.full_name),
  )


def cpp_type_to_c_ref(cpp_type: cpp.Type) -> cpp.Type:
  if cpp_type.is_builtin_structure: return builtins.get_builtin_structure(cpp_type).ref_type
  if cpp_type.is_decl_enum: return cpp_type.as_enum.as_c.type
  if cpp_type.is_decl_structure: return cpp_type.as_structure.as_c.ref_type

  return cpp.Type(
    base_name=utils.cpp_name_to_c_name(cpp_type.full_name),
  )
