from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from .. import cpp
from ... import utils


@dataclass
# Represents a C structure for a C++ struct/class.
class Structure:
  base: cpp.Structure

  @property
  def base_name(self) -> str: return utils.cpp_name_to_c_name(self.base.full_name)

  @property
  def name(self) -> str: return f'{self.base_name}_t'

  @property
  def ref_base_name(self) -> str: return f'{self.base_name}_ref'

  @property
  def ref_name(self) -> str: return f'{self.ref_base_name}_t'

  @property
  def create_methods(self) -> list[cpp.Method]:
    from ...converter.structure_converter import cpp_structure_create_methods
    return cpp_structure_create_methods(self)

  @property
  def destroy_method(self) -> Optional[cpp.Method]:
    from ...converter.structure_converter import cpp_structure_destroy_method
    return cpp_structure_destroy_method(self)

  @property
  def unwrap_method(self) -> cpp.Method:
    from ...converter.structure_converter import cpp_structure_unwrap_method
    return cpp_structure_unwrap_method(self)
  
  @property
  def copy_method(self) -> cpp.Method:
    from ...converter.structure_converter import cpp_structure_copy_method
    return cpp_structure_copy_method(self)

  @property
  def field_methods(self) -> dict[str, tuple[Optional[cpp.Method], Optional[cpp.Method]]]:
    from ...converter.structure_converter import cpp_structure_fields_to_c
    return cpp_structure_fields_to_c(self)

  @property
  def methods(self) -> list[cpp.Method]:
    from ...converter.structure_converter import cpp_structure_methods_to_c
    return cpp_structure_methods_to_c(self)

  @property
  def all_methods(self) -> list[cpp.Method]:
    res = []
    res.extend(self.create_methods)
    res.append(self.destroy_method)
    res.append(self.unwrap_method)
    res.append(self.copy_method)
    for getter, setter in self.field_methods.values():
      if getter: res.append(getter)
      if setter: res.append(setter)

    res.extend(self.methods)
    return res

  @property
  def type(self) -> cpp.Type:
    return cpp.Type(base_name=self.base_name, suffix='_t', cdecl_=self)

  @property
  def ref_type(self) -> cpp.Type:
    return cpp.Type(base_name=self.ref_base_name, suffix='_t', cdecl_=self)

  def unwrap_ref_type(self, var_name: str) -> str: return f'{self.ref_base_name}::unwrap({var_name})'
  def unwrap_type(self, var_name: str) -> str: return f'{self.base_name}::unwrap({var_name})'

  def wrap_ref_type(self, var_name: str) -> str: return f'{self.ref_base_name}::wrap(new ref<{self.base.full_name}>({var_name}))'
  def wrap_type(self, var_name: str) -> str: return f'{self.base_name}::wrap({var_name})'
