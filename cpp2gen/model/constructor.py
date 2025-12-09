from __future__ import annotations

from dataclasses import dataclass

from .method import Method


@dataclass
# A semantic representation of constructor for a structure.
class Constructor(Method):
  name: str = ''
  index: int = 0  # index of this constructor among all constructors of the parent structure
