from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .container import Container


@dataclass
# A semantic representation of a single enum value.
class EnumValue:
  name: str
  index: int
  parent: 'Enum'
  value: Optional[int] = None  # optional int value


@dataclass
# A semantic representation of an enum.
class Enum(Container):
  @property
  def values(self) -> list[EnumValue]: return [c for c in self.children if isinstance(c, EnumValue)]
