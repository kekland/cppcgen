from __future__ import annotations

from clang import cindex
from typing import Optional

from ..utils import traverse_cursor
from ...model import Method, Container
from ...utils import get_logger

logger = get_logger(__name__)


def parse_method(cursor: cindex.Cursor, parent: Container) -> Method:
  from .type_parser import parse_type
  from .parameter_parser import parse_parameters
  logger.debug(f'parsing method: {cursor.spelling} @ {cursor.location}')

  return Method(
    name=cursor.spelling,
    return_type=parse_type(cursor.result_type),
    parameters=parse_parameters(cursor),
    is_const=cursor.is_const_method(),
    is_static=cursor.is_static_method(),
    is_virtual=cursor.is_virtual_method(),
    is_pure_virtual=cursor.is_pure_virtual_method(),
    is_explicit=cursor.is_explicit_method(),
    is_inline=False,
    is_operator=cursor.spelling.startswith('operator'),  # A bit naive, but works for now.
    parent=parent,
  )


def parse_methods(cursor: cindex.Cursor, parent: Container) -> list[Method]:
  logger.debug(f'parsing methods for cursor: {cursor.spelling} @ {cursor.location}')
  methods: list[Method] = []

  def on_method(child_cursor: cindex.Cursor) -> bool:
    methods.append(parse_method(child_cursor, parent))
    return True

  traverse_cursor(
    cursor,
    on_method=on_method,
  )

  def find_methods(name: str) -> list[Method]: return [m for m in methods if m.name == name]

  for method in methods:
    overloads = find_methods(method.name)
    if len(overloads) > 1:
      for index, overload in enumerate(overloads):
        overload.index = index

  return methods
