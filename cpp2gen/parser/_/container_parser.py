from __future__ import annotations

from clang import cindex

from ..utils import traverse_cursor
from ...model import Container, Element
from ...utils import get_logger

logger = get_logger(__name__)


def parse_container_children(cursor: cindex.Cursor, parent: Container) -> list[Element]:
  logger.debug(f'parsing container children for cursor: {cursor.spelling} @ {cursor.location}')
  children: list[Element] = []

  from .constructor_parser import parse_constructors
  from .enum_parser import parse_enum
  from .field_parser import parse_field
  from .method_parser import parse_methods
  from .namespace_parser import parse_namespace
  from .structure_parser import parse_structure
  from .synthetic_field_parser import filter_children_for_synthetic_fields

  traverse_cursor(
    cursor,
    on_namespace=lambda c: children.append(parse_namespace(c, parent)) or True,
    on_field=lambda c: children.append(parse_field(c, parent)) or True,
    on_struct=lambda c, typedef: children.append(parse_structure(c, typedef, parent)) or True,
    on_class=lambda c, typedef: children.append(parse_structure(c, typedef, parent)) or True,
    on_enum=lambda c: children.append(parse_enum(c, parent)) or True,
  )

  children.extend(parse_methods(cursor, parent))

  children, synthetic_fields = filter_children_for_synthetic_fields(parent, children)
  children.extend(synthetic_fields)

  children.extend(parse_constructors(cursor, parent))

  return children
