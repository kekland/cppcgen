from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .container import Container
from .type import Type
from .method import Method


@dataclass
# A semantic representation of a field/member variable.
class Field:
  name: str
  type: Optional[Type]
  parent: Optional[Container] = None  # parent container, if any
