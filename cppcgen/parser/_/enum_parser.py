from __future__ import annotations

from clang import cindex
from logging import getLogger

from ... import context, parser
from ...model import cpp

_logger = getLogger('enum_parser')


def parse_enum_value(cursor: cindex.Cursor) -> cpp.EnumValue:
  _logger.debug(f'Parsing enum value: {cursor.spelling} = {cursor.enum_value}')
  return cpp.EnumValue(
    cindex_cursor=cursor,
    name=cursor.spelling,
    value=cursor.enum_value,
  )


def parse_enum_values(cursor: cindex.Cursor) -> list[cpp.EnumValue]:
  enum_values: list[cpp.EnumValue] = []

  def on_enum_value(child_cursor: cindex.Cursor) -> bool:
    enum_values.append(parse_enum_value(child_cursor))
    return True

  parser.utils.traverse_cursor(cursor, on_enum_value=on_enum_value)
  return enum_values


def parse_enum(cursor: cindex.Cursor) -> cpp.Enum:
  _logger.debug(f'Parsing enum: {cursor.spelling}')
  e = cpp.Enum(
    cindex_cursor=cursor,
    name=cursor.spelling,
    namespace=parser.utils.get_cursor_namespace(cursor),
    values=parse_enum_values(cursor),
  )

  context.add_enum(e)
  _logger.debug(f'Parsed enum: {e.name} with {len(e.values)} values')
  return e
