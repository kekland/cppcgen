from __future__ import annotations

from clang import cindex
from logging import getLogger

from ... import context, parser
from ...model import cpp

_logger = getLogger('field_parser')


def parse_field(cursor: cindex.Cursor) -> cpp.Field:
  _logger.debug(f'Parsing field: {cursor.spelling}')
  f = cpp.Field(
    cindex_cursor=cursor,
    name=cursor.spelling,
    type=parser.parse_type(cursor.type),
  )

  return f


def parse_fields(cursor: cindex.Cursor) -> list[cpp.Field]:
  fields: list[cpp.Field] = []

  def on_field(child_cursor: cindex.Cursor) -> bool:
    fields.append(parse_field(child_cursor))
    return True

  parser.utils.traverse_cursor(cursor, on_field=on_field)
  return fields
