from __future__ import annotations

from clang import cindex

from . import CppElement
from ..utils import traverse_cursor
from ...model import EnumValue, Enum, Container
from ...utils import get_logger

logger = get_logger(__name__)


class CppEnum(Enum, CppElement): pass


def parse_enum_value(cursor: cindex.Cursor, index: int, parent: Enum) -> EnumValue:
  logger.debug(f'parsing enum value: {cursor.spelling} = {cursor.enum_value} @ {cursor.location}')
  return EnumValue(
    index=index,
    name=cursor.spelling,
    value=cursor.enum_value,
    parent=parent,
  )


def parse_enum_values(cursor: cindex.Cursor, parent: Enum) -> list[EnumValue]:
  logger.debug(f'parsing enum values for: {cursor.spelling} @ {cursor.location}')
  enum_values: list[EnumValue] = []
  index = 0

  def on_enum_value(child_cursor: cindex.Cursor) -> bool:
    nonlocal index
    enum_values.append(parse_enum_value(child_cursor, index, parent))
    index += 1
    return True

  traverse_cursor(cursor, on_enum_value=on_enum_value)
  return enum_values


def parse_enum(cursor: cindex.Cursor, parent: Container) -> Enum:
  logger.debug(f'parsing enum: {cursor.spelling} @ {cursor.location}')
  enum = CppEnum(
    name=cursor.spelling,
    parent=parent,
  )

  enum.children.extend(parse_enum_values(cursor, enum))
  return enum
