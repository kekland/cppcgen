from __future__ import annotations

from clang import cindex
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from .. import context
from ..parser import utils as pu

from .field import Field
if TYPE_CHECKING:
  from .method import Method
  from .type import Type


@dataclass
# Represents a C++ "synthetic" field - a field that does not exist in the source code,
# but is semantically inferred, e.g. a getter/setter pair for a private field.
class SyntheticField(Field):
  getter: Optional[Method] = field(default=None)
  setter: Optional[Method] = field(default=None)
  cindex_cursor: Optional[cindex.Cursor] = field(init=False, repr=False, default=None)
  type: Optional[Type] = field(init=False, default=None)
