from __future__ import annotations

from clang import cindex
from logging import getLogger

from ... import context, parser
from ...model import cpp

_logger = getLogger('parameter_parser')

def parse_parameter(cursor: cindex.Cursor, index: int = 0) -> cpp.Parameter:
  _logger.debug(f'Parsing parameter: {cursor.spelling or f"p{index}"}, type: {cursor.type.spelling}')
  name = cursor.spelling
  if not name: name = f'p{index}'

  f = cpp.Parameter(
    cindex_cursor=cursor,
    name=name,
    type=parser.parse_type(cursor.type),
    default_value=parser.utils.get_default_value(cursor),
  )

  return f


def parse_parameters(cursor: cindex.Cursor) -> list[cpp.Parameter]:
  parameters: list[cpp.Parameter] = []
  param_index = 0

  def on_parameter(child_cursor: cindex.Cursor) -> bool:
    nonlocal param_index
    parameters.append(parse_parameter(child_cursor, param_index))
    param_index += 1
    return True

  parser.utils.traverse_cursor(cursor, on_parameter=on_parameter)
  return parameters
