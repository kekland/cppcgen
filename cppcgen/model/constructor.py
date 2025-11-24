from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .method import Method


@dataclass
# Represents a C++ constructor.
class Constructor(Method):
  name: str = field(init=False, default='')
  index: int = 0  # Index of the constructor in the structure

  @property
  def is_default(self) -> bool:
    assert self.cindex_cursor is not None
    return self.cindex_cursor.is_default_constructor()

  @property
  def is_regular(self) -> bool: return not self.is_copy and not self.is_move

  @property
  def is_copy(self) -> bool:
    assert self.cindex_cursor is not None
    return self.cindex_cursor.is_copy_constructor() or _is_copy_constructor(self)

  @property
  def is_move(self) -> bool:
    assert self.cindex_cursor is not None
    return self.cindex_cursor.is_move_constructor() or _is_move_constructor(self)


# Helper to determine if a constructor is a copy constructor.
#
# A copy constructor type looks like T::T(const T&).
def _is_copy_constructor(constructor: Constructor) -> bool:
  params = constructor.parameters
  if len(params) != 1: return False
  type = params[0].type

  assert constructor.parent is not None

  is_ref_correct = type.is_lvalue_reference and type.pointee.is_const and not type.pointee.is_pointer_or_reference
  is_return_correct = type.unqualified.cindex_decl_usr == constructor.parent.cindex_usr
  return is_ref_correct and is_return_correct


# Helper to determine if a constructor is a move constructor.
#
# A move constructor type looks like T::T(T&&).
def _is_move_constructor(constructor: Constructor) -> bool:
  params = constructor.parameters
  if len(params) != 1: return False
  type = params[0].type

  assert constructor.parent is not None

  is_ref_correct = type.is_rvalue_reference and not type.pointee.is_const and not type.pointee.is_pointer_or_reference
  is_return_correct = type.unqualified.cindex_decl_usr == constructor.parent.cindex_usr
  return is_ref_correct and is_return_correct
