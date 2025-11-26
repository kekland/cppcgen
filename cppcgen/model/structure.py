from __future__ import annotations

from clang import cindex
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from .. import utils
from .type import Type

if TYPE_CHECKING:
  from .method import Method
  from .field import Field
  from .synthetic_field import SyntheticField
  from .constructor import Constructor
  from . import c


@dataclass
# Represents a C++ struct or class.
class Structure:
  name: str  # name of the struct/class, without namespace
  namespace: str = ''
  cindex_cursor: Optional[cindex.Cursor] = field(default=None, repr=False)
  methods: list[Method] = field(default_factory=list)
  fields: list[Field] = field(default_factory=list)
  synthetic_fields: list[SyntheticField] = field(default_factory=list)
  constructors: list[Constructor] = field(default_factory=list)
  base_structures: list[Structure] = field(default_factory=list)
  c_structure_: Optional[c.Structure] = field(default=None, repr=False)
  type_: Optional[Type] = field(default=None, repr=False)

  @property
  def cindex_usr(self) -> Optional[str]: return self.cindex_cursor.get_usr() if self.cindex_cursor else None

  @property
  def is_abstract(self) -> bool: return any(m.is_pure_virtual for m in self.methods)

  @property
  def full_name(self) -> str: return utils.join_namespace(self.namespace, self.name)

  @property
  def default_constructor(self) -> Optional[Constructor]:
    for ctor in self.constructors:
      if ctor.is_default: return ctor
    return None

  @property
  def static_methods(self) -> list[Method]: return [m for m in self.methods if m.is_static]

  @property
  def instance_methods(self) -> list[Method]: return [m for m in self.methods if not m.is_static]

  @property
  def regular_constructors(self) -> list[Constructor]: return [ctor for ctor in self.constructors if ctor.is_regular]

  @property
  def type(self) -> Type:
    if self.type_ is not None: return self.type_
    if self.cindex_cursor is not None:
      from ..parser import parse_type
      return parse_type(self.cindex_cursor.type)

    return Type(
      base_name=self.name,
      namespace=self.namespace,
      cindex_type=self.cindex_cursor.type if self.cindex_cursor else None,
      cppdecl_=self,
    )

  @property
  def as_c(self):
    if self.c_structure_ is not None: return self.c_structure_
    from ..converter import cpp_structure_to_c
    return cpp_structure_to_c(self)
