from __future__ import annotations

from clang import cindex

from ..utils import traverse_cursor
from ...model import Field, Container
from ...utils import get_logger

logger = get_logger(__name__)


def parse_field(cursor: cindex.Cursor, parent: Container) -> Field:
  from .type_parser import parse_type
  logger.debug(f'parsing field: {cursor.spelling}, type: {cursor.type.spelling} @ {cursor.location}')

  return Field(
    name=cursor.spelling,
    type=parse_type(cursor.type),
    parent=parent,
  )


def parse_fields(cursor: cindex.Cursor, parent: Container) -> list[Field]:
  logger.debug(f'parsing fields for cursor: {cursor.spelling} @ {cursor.location}')
  fields: list[Field] = []

  def on_field(child_cursor: cindex.Cursor) -> bool:
    fields.append(parse_field(child_cursor, parent))
    return True

  traverse_cursor(
    cursor,
    on_field=on_field,
  )

  return fields
