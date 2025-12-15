from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Any

from .element import Element
from .type import Type


@dataclass
# A semantic representation of a container (namespace or class/struct) that can hold other entities.
class Container(Element):
  type_: Optional[Type] = None  # associated type representation, if any
  parent: Optional['Container'] = None  # parent container, if any
  children: list[Element] = field(default_factory=list)  # child entities contained in this container

  @property
  def type(self) -> Type:
    if self.type_ is not None: return self.type_
    return Type(base_name=self.name, namespace=self.namespace, decl_repr_=self)

  @property
  def type_ptr(self) -> Type: return Type(base_name=self.name, namespace=self.namespace, decl_repr_=self, is_pointer=True)

  # Find a direct child by name.
  def find_child(self, name: str) -> Optional[Element]:
    for child in self.children:
      if child.name == name: return child

    return None

  # Recursively find a child by a given path.
  def find_child_by_path(self, path: list[str]) -> Optional[Element]:
    if not path: return None
    first, *rest = path
    child = self.find_child(first)
    if child is None: return None
    if not rest: return child
    if not isinstance(child, Container): return None
    return child.find_child_by_path(rest)

  # Merge other container's children into this one.
  def merge(self, other: Container) -> None:
    for c in other.children:
      existing = self.find_child(c.name)

      # If both are containers, merge them recursively.
      if existing and isinstance(existing, Container) and isinstance(c, Container):
        existing.merge(c)

      # Otherwise, just add the new child (if not already present).
      elif not existing:
        self.children.append(c)

  @property
  def namespace(self) -> list[str]:
    if self.parent: return self.parent.full_name
    return []

  @property
  def full_name(self) -> list[str]:
    if self.parent: return [*self.parent.full_name, self.name]
    if self.name: return [self.name]
    return []

  @property
  def full_name_cpp_str(self) -> str: return '::'.join(self.full_name)

  @property
  def full_name_underscored(self) -> str: return '_'.join(self.full_name)

  def __repr_keys__(self): return [*super().__repr_keys__(), 'name']
