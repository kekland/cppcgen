from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .container import Container
from .element import Element
from .type import Type
from .method import Method


@dataclass
# A semantic representation of a field/member variable.
class Field(Element):
  name: str
  type: Optional[Type]
  parent: Optional[Container] = None  # parent container, if any
  getter: Optional[Method] = field(default=None)
  setter: Optional[Method] = field(default=None)

  def __repr_keys__(self): return [*super().__repr_keys__(), 'name', 'type']
