from __future__ import annotations

from clang import cindex

from ..utils import traverse_cursor
from ...model import Constructor, Container
from ...utils import get_logger

logger = get_logger(__name__)


def parse_constructor(cursor: cindex.Cursor, index: int, parent: Container) -> Constructor:
  from .parameter_parser import parse_parameters
  logger.debug(f'parsing constructor: {cursor.spelling} @ {cursor.location}')

  ctor = Constructor(
    name='',
    return_type=parent.type,
    parameters=parse_parameters(cursor),
    index=index,
    is_explicit=cursor.is_explicit_method(),
    parent=parent,
  )

  ctor.is_copy = _is_copy_constructor(ctor)
  ctor.is_move = _is_move_constructor(ctor)

  return ctor


def parse_constructors(cursor: cindex.Cursor, parent: Container) -> list[Constructor]:
  logger.debug(f'parsing constructors for: {cursor.spelling} @ {cursor.location}')
  ctors: list[Constructor] = []
  index = 0

  def on_constructor(child_cursor: cindex.Cursor) -> bool:
    nonlocal index
    ctors.append(parse_constructor(child_cursor, index, parent))
    index += 1
    return True

  traverse_cursor(cursor, on_constructor=on_constructor)

  # Implicit default constructor
  if len(ctors) == 0:
    ctors.append(Constructor(name='', return_type=parent.type, parameters=[], index=0, parent=parent))

  return ctors

# Helper to determine if a constructor is a copy constructor.
#
# A copy constructor type looks like T::T(const T&).


def _is_copy_constructor(constructor: Constructor) -> bool:
  params = constructor.parameters
  if len(params) != 1: return False
  type = params[0].type

  assert constructor.parent is not None

  is_ref_correct = type.is_lvalue_reference and type.is_const
  return is_ref_correct


# Helper to determine if a constructor is a move constructor.
#
# A move constructor type looks like T::T(T&&).
def _is_move_constructor(constructor: Constructor) -> bool:
  params = constructor.parameters
  if len(params) != 1: return False
  type = params[0].type

  assert constructor.parent is not None

  is_ref_correct = type.is_rvalue_reference and not type.is_const
  return is_ref_correct
