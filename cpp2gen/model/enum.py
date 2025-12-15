from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .container import Container
from .element import Element


@dataclass
# A semantic representation of a single enum value.
class EnumValue(Element):
  index: int
  name: str
  parent: 'Enum'
  value: Optional[int] = None  # optional int value

  def __repr_keys__(self): return [*super().__repr_keys__(), 'name', 'index', 'value']


@dataclass
# A semantic representation of an enum.
class Enum(Container):
  name: str

  @property
  def values(self) -> list[EnumValue]: return [c for c in self.children if isinstance(c, EnumValue)]

  def __repr_keys__(self): return [*super().__repr_keys__(), 'values']
