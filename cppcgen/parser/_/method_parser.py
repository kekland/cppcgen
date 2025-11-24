from __future__ import annotations

from clang import cindex
from logging import getLogger

from ... import context, parser
from ...model import cpp

_logger = getLogger('method_parser')

def parse_method(cursor: cindex.Cursor) -> cpp.Method:
  _logger.debug(f'Parsing method: {cursor.spelling}')
  f = cpp.Method(
    cindex_cursor=cursor,
    name=cursor.spelling,
    return_type=parser.parse_type(cursor.result_type),
    parameters=parser.parse_parameters(cursor),
    is_const=cursor.is_const_method(),
    is_static=cursor.is_static_method(),
    is_virtual=cursor.is_virtual_method(),
    is_pure_virtual=cursor.is_pure_virtual_method(),
    is_explicit=cursor.is_explicit_method(),
    is_inline=False,  # TODO
  )

  return f


def parse_methods(cursor: cindex.Cursor) -> list[cpp.Method]:
  methods: list[cpp.Method] = []

  def on_method(child_cursor: cindex.Cursor) -> bool:
    methods.append(parse_method(child_cursor))
    return True

  parser.utils.traverse_cursor(cursor, on_method=on_method)
  return methods
