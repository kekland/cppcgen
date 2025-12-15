from __future__ import annotations

from clang import cindex
from typing import Optional

from . import CppElement
from .method_parser import parse_method
from ..utils import traverse_cursor
from ...model import Namespace, Container, Element, Structure
from ...utils import get_logger

logger = get_logger(__name__)


class CppStructure(Structure, CppElement): pass


def parse_structure(cursor: cindex.Cursor, typedef_cursor: Optional[cindex.Cursor], parent: Container) -> Structure:
  from .container_parser import parse_container_children
  from .type_parser import parse_type
  logger.debug(f'parsing structure: {cursor.spelling} @ {cursor.location}')
  structure = CppStructure(
    name=(typedef_cursor or cursor).spelling,
    parent=parent,
    type_=parse_type((typedef_cursor or cursor).type),
  )

  structure.children.extend(parse_container_children(cursor, structure))
  return structure
