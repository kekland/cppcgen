from __future__ import annotations

from clang import cindex
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from .. import context
from ..parser import utils as pu

if TYPE_CHECKING:
  from .type import Type


@dataclass
# Represents a C++ parameter.
class Parameter:
  name: str
  type: Type
  default_value: Optional[str] = None
  cindex_cursor: Optional[cindex.Cursor] = field(default=None, repr=False)

  @property
  def cindex_usr(self) -> Optional[str]: return self.cindex_cursor.get_usr() if self.cindex_cursor else None

  @property
  def as_c(self):
    from ..converter import cpp_parameter_to_c
    return cpp_parameter_to_c(self)
