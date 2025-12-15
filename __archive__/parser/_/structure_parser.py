from __future__ import annotations

from clang import cindex
from typing import Optional
from logging import getLogger

from ... import context, parser, utils
from ...model import cpp

_logger = getLogger('structure_parser')


def parse_base_structures(cursor: cindex.Cursor) -> list[cpp.Structure]:
  return []  # unused for now


def parse_structure(cursor: cindex.Cursor, type_alias_cursor: Optional[cindex.Cursor] = None) -> cpp.Structure:
  _logger.debug(f'Parsing structure: {(type_alias_cursor or cursor).spelling}')
  s = cpp.Structure(
    cindex_cursor=cursor,
    name=(type_alias_cursor or cursor).spelling,
    namespace=parser.utils.get_cursor_namespace(type_alias_cursor or cursor),
    fields=parser.parse_fields(cursor),
    base_structures=parse_base_structures(cursor),
    type_=parser.parse_type(type_alias_cursor.type) if type_alias_cursor else None,
  )

  methods, synthetic_fields = parser.filter_methods_for_synthetic_fields(s, parser.parse_methods(cursor))
  s.methods = methods
  s.synthetic_fields = list(synthetic_fields)

  # merge/clean public fields and synthetic fields for them
  for synth in synthetic_fields:
    for field in s.fields:
      if utils.cpp_name_to_c_name(field.name) == utils.cpp_name_to_c_name(synth.name):
        field.getter = synth.getter
        field.setter = synth.setter
        s.synthetic_fields.remove(synth)
        _logger.debug(f'Merged synthetic field {synth.name} into public field')
        break


  s.constructors = parser.parse_constructors(cursor, s)

  context.add_structure(s)
  _logger.debug(
    f'Parsed structure: {s.name} with {len(s.fields)} fields, {len(s.methods)} methods, {len(s.synthetic_fields)} synth, {len(s.constructors)} ctors')
  return s
