from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .. import cpp
from ... import utils


@dataclass
# Represents a C enum value for a C++ enum value.
class EnumValue:
  base: cpp.EnumValue

  @property
  def name(self) -> str: return utils.cpp_name_to_c_name(self.base.full_name).upper()

  @property
  def value(self) -> int: return self.base.value


@dataclass
# Represents a C enum for a C++ enum.
class Enum:
  base: cpp.Enum

  @property
  def name(self) -> str: return utils.cpp_name_to_c_name(self.base.full_name).upper()

  @property
  def values(self) -> list[EnumValue]: return [EnumValue(base=v) for v in self.base.values]

  @property
  def to_c_fn(self) -> cpp.Method:
    from ...converter.enum_converter import cpp_enum_to_c_fn
    return cpp_enum_to_c_fn(self.base)

  @property
  def from_c_fn(self) -> cpp.Method:
    from ...converter.enum_converter import cpp_enum_from_c_fn
    return cpp_enum_from_c_fn(self.base)

  @property
  def type(self) -> cpp.Type:
    return cpp.Type(base_name=self.name, cdecl_=self)
