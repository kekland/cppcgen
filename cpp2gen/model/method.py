from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .container import Container
from .type import Type
from .parameter import Parameter


@dataclass
# A semantic representation of a method/function.
class Method:
  name: str
  return_type: Type
  parameters: list[Parameter] = field(default_factory=list)
  parent: Optional[Container] = None  # parent container, if any
  impl: Optional[list[str]] = None  # implementation code lines, if any

  is_const: bool = False
  is_static: bool = False
  is_inline: bool = False
  is_virtual: bool = False
  is_pure_virtual: bool = False
  is_explicit: bool = False
