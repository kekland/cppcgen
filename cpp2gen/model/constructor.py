from __future__ import annotations

from dataclasses import dataclass

from .method import Method


@dataclass
# A semantic representation of constructor for a structure.
class Constructor(Method):
  index: int | None = 0  # index of this constructor among all constructors of the parent structure
  is_static: bool = True
  is_move: bool = False
  is_copy: bool = False

  def __repr_keys__(self): return [*super().__repr_keys__(), 'index']
