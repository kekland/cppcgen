from __future__ import annotations

from clang import cindex
from logging import getLogger

from ... import context, parser
from ...model import cpp

_logger = getLogger('constructor_parser')


def parse_constructor(cursor: cindex.Cursor, index: int, parent: cpp.Structure) -> cpp.Constructor:
  _logger.debug(f'Parsing constructor: {parent.name}::{cursor.spelling}')
  ctor = cpp.Constructor(
    cindex_cursor=cursor,
    index=index,
    parameters=parser.parse_parameters(cursor),
    return_type=parent.type,
    is_explicit=cursor.is_explicit_method(),
  )

  return ctor


def parse_constructors(cursor: cindex.Cursor, parent: cpp.Structure) -> list[cpp.Constructor]:
  ctors: list[cpp.Constructor] = []
  ctor_index = 0

  def on_constructor(child_cursor: cindex.Cursor) -> bool:
    nonlocal ctor_index
    ctors.append(parse_constructor(child_cursor, ctor_index, parent))
    ctor_index += 1
    return True

  parser.utils.traverse_cursor(cursor, on_constructor=on_constructor)
  return ctors
