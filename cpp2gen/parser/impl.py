import pathlib

from clang import cindex

from .libclang import configure_libclang, parse_translation_unit
from .utils import traverse_cursor
from ..context import Context


def parse_file(path: pathlib.Path, include_dirs: list[pathlib.Path] = []) -> Context:
  ctx = Context()
  tu = parse_translation_unit(path, include_dirs)
  assert tu.cursor is not None

  from ._.namespace_parser import parse_namespace
  from ._.structure_parser import parse_structure
  from ._.enum_parser import parse_enum

  traverse_cursor(
    tu.cursor,
    on_namespace=lambda c: ctx.children.append(parse_namespace(c, ctx)) or True,
    on_struct=lambda c, typedef: ctx.children.append(parse_structure(c, typedef, ctx)) or True,
    on_class=lambda c, typedef: ctx.children.append(parse_structure(c, typedef, ctx)) or True,
    on_enum=lambda c: ctx.children.append(parse_enum(c, ctx)) or True,
  )

  return ctx
