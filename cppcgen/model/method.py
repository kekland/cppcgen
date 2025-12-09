from __future__ import annotations

from clang import cindex
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from .. import context
from ..parser import utils as pu
from .. import utils

if TYPE_CHECKING:
  from .parameter import Parameter
  from .type import Type
  from .structure import Structure


@dataclass
# Represents a C++ method/function.
class Method:
  name: str
  return_type: Type
  namespace: str = ''
  parameters: list[Parameter] = field(default_factory=list)
  cindex_cursor: Optional[cindex.Cursor] = field(default=None, repr=False)
  parent_: Optional[Structure] = field(default=None, repr=False)
  base: Optional[Method] = field(default=None, repr=False)
  parent_name_prefix: Optional[str] = field(default=None, repr=False)

  is_const: bool = False
  is_static: bool = False
  is_inline: bool = False
  is_virtual: bool = False
  is_pure_virtual: bool = False
  is_explicit: bool = False

  impl: Optional[list[str]] = None

  @property
  def cindex_usr(self) -> Optional[str]: return self.cindex_cursor.get_usr() if self.cindex_cursor else None

  @property
  def parent(self) -> Optional[Structure]:
    if self.parent_ is not None: return self.parent_
    if self.cindex_cursor is not None:
      if self.cindex_cursor.semantic_parent is not None:
        return context.get_structure_by_usr(pu.unsafe_get_semantic_parent_cursor(self.cindex_cursor).get_usr())

    return None

  @property
  def is_global(self) -> bool: return self.parent_ is None

  @property
  def unprefixed_name(self) -> str:
    if self.parent_name_prefix is not None and self.name.startswith(self.parent_name_prefix): return self.name[len(self.parent_name_prefix):]
    return self.name

  @property
  def full_name(self) -> str:
    if self.parent is not None: return f'{self.parent.full_name}::{self.name}'
    return utils.join_namespace(self.namespace, self.name)

  @property
  def call_name(self) -> str:
    if self.parent is not None and self.is_static: return f'{self.parent.full_name}::{self.name}'
    if self.namespace: return utils.join_namespace(self.namespace, self.name)
    return self.name

  @property
  def as_c(self) -> Method:
    from ..converter import cpp_method_to_c
    return cpp_method_to_c(self)

  @property
  def is_operator(self) -> bool:
    return self.name.startswith('operator')  # A bit naive, but works for now.

  def generate_decl(self) -> list[str]:
    from ..generator import generate_method_decl
    return generate_method_decl(self)

  def generate_impl(self, impl: Optional[list[str]] = None) -> list[str]:
    from ..generator import generate_method_impl
    return generate_method_impl(self, impl)

  def generate_call(self, param_names: Optional[list[str]] = None, param_suffix: Optional[str] = '_') -> str:
    from ..generator import generate_method_call
    return generate_method_call(self, param_names, param_suffix)
