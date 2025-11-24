from ._.constructor_parser import parse_constructor, parse_constructors
from ._.enum_parser import parse_enum_value, parse_enum_values, parse_enum
from ._.field_parser import parse_field, parse_fields
from ._.method_parser import parse_method, parse_methods
from ._.parameter_parser import parse_parameter, parse_parameters
from ._.structure_parser import parse_structure
from ._.synthetic_field_parser import filter_methods_for_synthetic_fields
from ._.type_parser import parse_type
from . import utils

__all__ = [
  'parse_constructor',
  'parse_constructors',
  'parse_enum_value',
  'parse_enum_values',
  'parse_enum',
  'parse_field',
  'parse_fields',
  'parse_method',
  'parse_methods',
  'parse_parameter',
  'parse_parameters',
  'parse_structure',
  'filter_methods_for_synthetic_fields',
  'parse_type',
  'utils',
]

import pathlib
from clang import cindex
from typing import Optional, Union

from .. import context, libclang
from ..model import cpp


def _traverse_cursor(cursor: cindex.Cursor) -> list[Union[cpp.Structure, cpp.Enum]]:
  met_entities: list[Union[cpp.Structure, cpp.Enum]] = []

  def _handle_enum(cursor: cindex.Cursor):
    if context.has_enum_by_usr(cursor.get_usr()): return
    e = parse_enum(cursor)
    met_entities.append(e)
    return True

  def _handle_struct_or_class(cursor: cindex.Cursor, type_alias_cursor: Optional[cindex.Cursor] = None):
    if context.has_structure_by_usr(cursor.get_usr()): return
    s = parse_structure(cursor, type_alias_cursor)
    met_entities.append(s)
    return False  # Classes/structures can contain other classes/structures

  utils.traverse_cursor(
    cursor,
    on_enum=_handle_enum,
    on_struct=_handle_struct_or_class,
    on_class=_handle_struct_or_class,
  )

  return met_entities


def parse_file(file_path: pathlib.Path, include_dirs: list[pathlib.Path] = []) -> list[Union[cpp.Structure, cpp.Enum]]:
  tu = libclang.parse_translation_unit(file_path, include_dirs)
  assert tu.cursor is not None
  return _traverse_cursor(tu.cursor)
