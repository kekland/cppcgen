from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .element import Element
from .container import Container
from .type import Type
from .parameter import Parameter


@dataclass
# A semantic representation of a method/function.
class Method(Element):
  return_type: Type
  parameters: list[Parameter] = field(default_factory=list)
  parent: Optional[Container] = None  # parent container, if any
  impl: Optional[list[str]] = None  # implementation code lines, if any
  index: Optional[int] = None  # index for method overloads, if multiple are present

  is_const: bool = False
  is_static: bool = False
  is_inline: bool = False
  is_virtual: bool = False
  is_pure_virtual: bool = False
  is_explicit: bool = False
  is_getter: bool = False
  is_setter: bool = False
  is_operator: bool = False

  @property
  def full_name_cpp_str(self) -> str:
    if self.parent: return f'{self.parent.full_name_cpp_str}::{self.name}'
    return self.name

  @property
  def full_name(self) -> list[str]:
    if self.parent: return [*self.parent.full_name, self.name]
    return [self.name]

  def __repr_keys__(self): return [*super().__repr_keys__(), 'name', 'return_type', 'parameters',
                                   'is_const', 'is_static', 'is_inline', 'is_virtual', 'is_pure_virtual', 'is_explicit']
