from __future__ import annotations

from clang import cindex

from ..utils import traverse_cursor
from ...model import Namespace, Container, Element
from ...utils import get_logger

logger = get_logger(__name__)


def parse_namespace(cursor: cindex.Cursor, parent: Container) -> Namespace:
  from .container_parser import parse_container_children
  logger.debug(f'parsing namespace: {cursor.spelling} @ {cursor.location}')
  namespace = Namespace(
    name=cursor.spelling,
    parent=parent,
  )

  namespace.children.extend(parse_container_children(cursor, namespace))
  return namespace
