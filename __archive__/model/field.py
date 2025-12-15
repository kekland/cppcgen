from __future__ import annotations

from clang import cindex
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from .. import context
from ..parser import utils as pu

if TYPE_CHECKING:
  from .type import Type
  from .structure import Structure
  from .method import Method

@dataclass
# Represents a C++ field (member variable).
class Field:
  name: str
  type: Optional[Type]
  cindex_cursor: Optional[cindex.Cursor] = field(default=None, repr=False)
  parent_: Optional[Structure] = field(default=None, repr=False)
  getter: Optional[Method] = field(default=None, init=False)
  setter: Optional[Method] = field(default=None, init=False)

  @property
  def cindex_usr(self) -> Optional[str]: return self.cindex_cursor.get_usr() if self.cindex_cursor else None

  @property
  def parent(self) -> Optional[Structure]:
    if self.parent_ is not None: return self.parent_
    if self.cindex_cursor is not None: return context.get_structure_by_usr(pu.unsafe_get_semantic_parent_cursor(self.cindex_cursor).get_usr())
    return None
