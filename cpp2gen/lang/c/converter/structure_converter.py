from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field

from ._base import CElement
from ..utils import to_c_name
from ....model import Structure, Method, Type
from ....builtins import BuiltinStructure
from ....utils import indent


class CStructure(Structure, CElement):
  base: Structure
  ref: CStructureRef

  @property
  def ptr_typedef_name(self) -> str: return f'{self.name}_t'

  @property
  def ref_destroy_method(self) -> Method: return self.ref.destroy_method

  @property
  def ref_unwrap_method(self) -> Method: return self.ref.unwrap_method

  @property
  def copy_method(self) -> Method: return _struct_copy_method(self)

  def unwrap(self, var_name: str) -> str: return f'{self.name}::unwrap({var_name})'
  def wrap(self, var_name: str) -> str: return f'{self.name}::wrap({var_name})'


class CStructureRef(Structure, CElement):
  base: CStructure

  @property
  def ptr_typedef_name(self) -> str: return f'{self.name}_t'

  @property
  def destroy_method(self) -> Method: return _struct_ref_destroy_method(self)

  @property
  def unwrap_method(self) -> Method: return _struct_ref_unwrap_method(self)

  def unwrap(self, var_name: str) -> str: return f'{self.name}::unwrap({var_name})'
  def wrap(self, var_name: str) -> str: return f'{self.name}::wrap(new ref<{self.base.base.full_name_cpp_str}>({var_name}))'


def convert_structure_lite(structure: Structure) -> CStructure:
  if isinstance(structure, CStructure): return structure
  if isinstance(structure, BuiltinStructure):
    if passthrough := structure.passthrough_type:
      return convert_structure_lite(passthrough.decl_repr)  # type:ignore

  new_structure = CStructure(name=to_c_name(structure.full_name))
  if hasattr(structure, 'c_name'): new_structure.name = structure.c_name  # type: ignore
  ref_structure = CStructureRef(name=new_structure.name + '_ref')
  ref_structure.base = new_structure

  new_structure.base = structure
  new_structure.ref = ref_structure
  new_structure.children = []

  return new_structure


def convert_structure(structure: Structure) -> CStructure:
  if isinstance(structure, CStructure): return structure

  new_structure = convert_structure_lite(structure)
  if isinstance(structure, BuiltinStructure):
    new_structure.children = [new_structure.copy_method, new_structure.ref_destroy_method, new_structure.ref_unwrap_method]
    return new_structure

  from . import convert_structure_method, convert_field

  field_methods: list[Method] = []
  for field in structure.all_fields:
    getter, setter = convert_field(field)
    if getter is not None: field_methods.append(getter)
    if setter is not None: field_methods.append(setter)

  new_structure.children = [
    new_structure.copy_method,
    new_structure.ref_destroy_method,
    new_structure.ref_unwrap_method,
    *[convert_structure_method(m) for m in structure.regular_constructors],
    *[convert_structure_method(m) for m in structure.factory_methods],
    *[convert_structure_method(m) for m in structure.static_nonfactory_methods],
    *[convert_structure_method(m) for m in structure.instance_methods],
    *field_methods,
  ]

  return new_structure


def _struct_ref_destroy_method(struct: CStructureRef) -> Method:
  impl = struct.unwrap('instance')

  return Method(
    name=f'{struct.name}_destroy',
    return_type=Type.void(),
    parameters=[struct.type_ptr.as_param('instance')],
    impl=[f'delete {impl};'],
  )


def _struct_ref_unwrap_method(struct: CStructureRef) -> Method:
  impl = struct.unwrap('instance')
  impl = f'{impl}->unwrap()'
  impl = struct.base.wrap(impl)

  return Method(
    name=f'{struct.name}_unwrap',
    return_type=struct.base.type_ptr,
    parameters=[struct.type_ptr.as_param('instance')],
    impl=[f'return {impl};'],
  )


def _struct_copy_method(struct: CStructure) -> Method:
  impl: list[str] = []
  impl.append(f'auto instance_ = {struct.unwrap("instance")};')
  impl.append(f'return {struct.ref.wrap(f"*instance_")};')

  return Method(
    name=f'{struct.name}_copy',
    return_type=struct.ref.type_ptr,
    parameters=[struct.type_ptr.as_param('instance')],
    impl=impl,
  )
