from __future__ import annotations

from clang import cindex
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from .. import context, utils
from ..parser import utils as pu
from .type import Type
from .method import Method


@dataclass
# Represents a C++ enum value.
class EnumValue:
  name: str
  value: int
  cindex_cursor: Optional[cindex.Cursor] = field(default=None, repr=False)
  parent_: Optional[Enum] = field(default=None, repr=False)

  @property
  def cindex_usr(self) -> Optional[str]: return self.cindex_cursor.get_usr() if self.cindex_cursor else None

  @property
  def parent(self) -> Enum:
    if self.parent_ is not None: return self.parent_
    if self.cindex_cursor is not None: return context.get_enum_by_usr(pu.unsafe_get_semantic_parent_cursor(self.cindex_cursor).get_usr())  # type: ignore
    raise ValueError("EnumValue has no parent enum")

  @property
  def full_name(self) -> str: return utils.join_namespace(self.parent.full_name, self.name)

  @property
  def as_c(self):
    from ..converter import cpp_enum_value_to_c
    return cpp_enum_value_to_c(self)


@dataclass
# Represents a C++ enum.
class Enum:
  name: str
  namespace: str = ''
  cindex_cursor: Optional[cindex.Cursor] = field(default=None, repr=False)
  values: list[EnumValue] = field(default_factory=list)

  @property
  def cindex_usr(self) -> Optional[str]: return self.cindex_cursor.get_usr() if self.cindex_cursor else None

  @property
  def full_name(self) -> str: return utils.join_namespace(self.namespace, self.name)

  @property
  def as_c(self):
    from ..converter import cpp_enum_to_c
    return cpp_enum_to_c(self)

  @property
  def from_c_fn(self) -> Method:
    from ..converter.enum_converter import cpp_enum_from_c_fn
    return cpp_enum_from_c_fn(self)

  @property
  def to_c_fn(self) -> Method:
    from ..converter.enum_converter import cpp_enum_to_c_fn
    return cpp_enum_to_c_fn(self)

  @property
  def type(self) -> Type:
    return Type(
      base_name=self.name,
      namespace=self.namespace,
      cindex_type=self.cindex_cursor.type if self.cindex_cursor else None,
      cppdecl_=self,
    )
