from __future__ import annotations

from typing import Optional

from ._base import DartElement
from ..utils import to_dart_top_level_name, to_dart_member_name
from ....model import Structure, Method, Constructor, Type


class DartStructure(Structure, DartElement):
  base: Structure

  @property
  def _base_non_factory_methods(self) -> list[Method]: return [*self.base.static_nonfactory_methods, *self.base.instance_methods]

  @property
  def _base_factory_methods(self) -> list[Method]: return [*self.base.factory_methods, *self.base.regular_constructors]

  @property
  def _base_methods(self) -> list[Method]: return [*self._base_factory_methods, *self._base_non_factory_methods]

  @property
  def methods(self) -> list[Method]:
    from .method_converter import convert_structure_method
    return [convert_structure_method(m) for m in self._base_non_factory_methods]

  @property
  def regular_constructors(self) -> list[Constructor]:
    from .method_converter import convert_structure_constructor
    return [convert_structure_constructor(m) for m in self._base_factory_methods]

  @property
  def ext_methods(self) -> list[Method]:
    from .method_converter import convert_structure_method_ext
    from .field_converter import convert_field_ext

    field_methods: list[Method] = []
    for f in self.base.all_fields:
      getter_ext, setter_ext = convert_field_ext(f)
      if getter_ext: field_methods.append(getter_ext)
      if setter_ext: field_methods.append(setter_ext)

    return [
      *[convert_structure_method_ext(m) for m in self._base_non_factory_methods],
      *field_methods,
    ]

  @property
  def ref_ext_methods(self) -> list[Method]:
    from .method_converter import convert_structure_method_ext_to_ref_ext, convert_structure_method_ext
    return [
      *[convert_structure_method_ext_to_ref_ext(convert_structure_method_ext(m)) for m in self._base_factory_methods],
      *[convert_structure_method_ext_to_ref_ext(m) for m in self.ext_methods],
    ]

  @property
  def field_methods(self) -> list[Method]:
    from .field_converter import convert_field
    methods: list[Method] = []
    for field in self.base.all_fields:
      getter, setter = convert_field(field)
      if getter: methods.append(getter)
      if setter: methods.append(setter)
    return methods


def convert_structure(value: Structure) -> DartStructure:
  new_structure = DartStructure(name=to_dart_top_level_name(value.name))
  new_structure.base = value

  return new_structure
