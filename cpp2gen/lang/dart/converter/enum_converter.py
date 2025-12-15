from __future__ import annotations

from typing import Optional

from ._base import DartElement
from ..utils import to_dart_top_level_name, to_dart_member_name
from ....model import EnumValue, Enum, Method


class DartEnum(Enum, DartElement):
  base: Enum

  @property
  def from_ffi_method(self) -> Method: return cpp_enum_to_dart_method(self.base)

  @property
  def to_ffi_method(self) -> Method: return cpp_enum_from_dart_method(self.base)


def convert_enum_value(value: EnumValue, parent: Optional[Enum] = None) -> EnumValue:
  return EnumValue(
    name=to_dart_member_name([value.name]),
    value=value.value,
    index=value.index,
    parent=parent or value.parent,
  )


def convert_enum(enum: Enum) -> DartEnum:
  new_enum = DartEnum(
    name=to_dart_top_level_name(enum.name),
  )

  new_enum.base = enum
  new_enum.children.extend([convert_enum_value(value, parent=new_enum) for value in enum.values])

  return new_enum


def cpp_enum_to_dart_method(enum: Enum) -> Method:
  from ...c import converter as c_converter
  c_enum = c_converter.convert_enum(enum)
  dart_enum = convert_enum(enum)

  impl = []
  impl.append(f'return switch (v) {{')
  for i in range(len(enum.values)):
    dart_v = dart_enum.values[i]
    c_v = c_enum.values[i]
    impl.append(f'  gen_ffi.{c_enum.name}.{c_v.name} => {dart_enum.name}.{dart_v.name},')
  impl.append(f'}};')

  return Method(
    name='fromFfi',
    parent=dart_enum,
    return_type=dart_enum.type,
    parameters=[c_enum.type.as_param('v')],
    is_static=True,
    impl=impl,
  )


def cpp_enum_from_dart_method(enum: Enum) -> Method:
  from ...c import converter as c_converter
  c_enum = c_converter.convert_enum(enum)
  dart_enum = convert_enum(enum)

  impl = []
  impl.append(f'return switch (this) {{')
  for i in range(len(enum.values)):
    dart_v = dart_enum.values[i]
    c_v = c_enum.values[i]
    impl.append(f'  {dart_enum.name}.{dart_v.name} => gen_ffi.{c_enum.name}.{c_v.name},')
  impl.append(f'}};')

  return Method(
    name='toFfi',
    parent=dart_enum,
    return_type=c_enum.type,
    impl=impl,
  )
