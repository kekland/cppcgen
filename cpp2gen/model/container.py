from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
# A semantic representation of a container (namespace or class/struct) that can hold other entities.
class Container:
  name: str
  parent: Optional['Container'] = None  # parent container, if any
  children: list[Any] = field(default_factory=list)  # child entities contained in this container

  @property
  def namespace(self) -> list[str]:
    if self.parent: return self.parent.full_name
    return []

  @property
  def full_name(self) -> list[str]:
    if self.parent: return [*self.parent.full_name, self.name]
    return [self.name]
