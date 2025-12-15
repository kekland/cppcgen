from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field

from ._base import CElement
from ..utils import to_c_name
from ....model import EnumValue, Enum, Method, Namespace
from ....utils import indent


class CEnum(Enum, CElement):
  base: Enum

  @property
  def to_c_method(self) -> Method: return _cpp_enum_to_c_method(self.base)

  @property
  def from_c_method(self) -> Method: return _c_enum_to_cpp_method(self.base)


def convert_enum_value(value: EnumValue, parent: Optional[Enum] = None) -> EnumValue:
  return EnumValue(
    name=to_c_name([*value.parent.full_name, value.name]).upper(),
    value=value.value,
    index=value.index,
    parent=parent or value.parent,
  )


def convert_enum(enum: Enum) -> CEnum:
  new_enum = CEnum(
    name=to_c_name(enum.full_name).upper(),
    parent=None,
  )

  new_enum.base = enum
  new_enum.children.extend([convert_enum_value(value, parent=new_enum) for value in enum.values])
  return new_enum


def _cpp_enum_to_c_method(enum: Enum) -> Method:
  c_enum = convert_enum(enum)

  cases: list[str] = []
  for i in range(len(enum.values)):
    v = enum.values[i]
    c_v = c_enum.values[i]
    cases.append(f'case {enum.full_name_cpp_str}::{v.name}: return {c_v.name};')

  return Method(
    name='to_c',
    parent=Namespace(name='enum_cv'),
    return_type=c_enum.type,
    parameters=[enum.type.as_param('value')],
    is_inline=True,
    impl=[
      f'switch (value) {{',
      *(indent(cases)),
      f'  default: std::abort();',
      f'}}',
    ],
  )


def _c_enum_to_cpp_method(enum: Enum) -> Method:
  c_enum = convert_enum(enum)

  cases: list[str] = []
  for i in range(len(enum.values)):
    v = enum.values[i]
    c_v = c_enum.values[i]
    cases.append(f'case {c_v.name}: return {enum.full_name_cpp_str}::{v.name};')

  return Method(
    name='from_c',
    parent=Namespace(name='enum_cv'),
    return_type=enum.type,
    parameters=[c_enum.type.as_param('value')],
    is_inline=True,
    is_static=True,
    impl=[
      f'switch (value) {{',
      *(indent(cases)),
      f'  default: std::abort();',
      f'}}',
    ],
  )
