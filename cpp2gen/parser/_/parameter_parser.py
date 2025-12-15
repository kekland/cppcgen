from __future__ import annotations

from clang import cindex

from .type_parser import parse_type
from ..utils import get_default_value, traverse_cursor
from ...model import Parameter
from ...utils import get_logger

logger = get_logger(__name__)


def parse_parameter(cursor: cindex.Cursor, index: int = 0) -> Parameter:
  logger.debug(f'parsing parameter: {cursor.spelling or f"p{index}"}, type: {cursor.type.spelling} @ {cursor.location}')

  has_name = cursor.spelling != ''

  return Parameter(
    type=parse_type(cursor.type),
    name=cursor.spelling if has_name else f'p{index}',
    is_name_synthetic=not has_name,
    default_value=get_default_value(cursor),
  )


def parse_parameters(cursor: cindex.Cursor) -> list[Parameter]:
  logger.debug(f'parsing parameters for cursor: {cursor.spelling} @ {cursor.location}')
  parameters: list[Parameter] = []
  index = 0

  def on_parameter(cursor: cindex.Cursor) -> bool:
    nonlocal index
    param = parse_parameter(cursor, index)
    parameters.append(param)
    index += 1
    return True
  
  for arg in cursor.get_arguments():
    assert arg is not None
    on_parameter(arg)

  return parameters
