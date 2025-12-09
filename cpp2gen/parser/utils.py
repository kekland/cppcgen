from __future__ import annotations

from clang import cindex
from typing import Union, Callable, Optional


# Recursively traverse the cursor tree.
#
# If a callback returns True, the traversal does not continue into the children of that cursor.
#
# For on_struct and on_class, the typedef cursor is also provided as the second argument (if it exists).
def traverse_cursor(
  cursor: cindex.Cursor,
  on_struct: Callable[[cindex.Cursor, Optional[cindex.Cursor]], Optional[bool]] = lambda c, _: False,
  on_class: Callable[[cindex.Cursor, Optional[cindex.Cursor]], Optional[bool]] = lambda c, _: False,
  on_base_specifier: Callable[[cindex.Cursor], Optional[bool]] = lambda c: True,
  on_constructor: Callable[[cindex.Cursor], Optional[bool]] = lambda c: True,
  on_enum: Callable[[cindex.Cursor], Optional[bool]] = lambda c: True,
  on_enum_value: Callable[[cindex.Cursor], Optional[bool]] = lambda c: True,
  on_method: Callable[[cindex.Cursor], Optional[bool]] = lambda c: True,
  on_parameter: Callable[[cindex.Cursor], Optional[bool]] = lambda c: True,
  on_field: Callable[[cindex.Cursor], Optional[bool]] = lambda c: True,
):
  def next_traverse(child_cursor: cindex.Cursor):
    traverse_cursor(child_cursor, on_struct, on_class, on_base_specifier, on_constructor, on_enum, on_enum_value, on_method, on_parameter, on_field)

  for child_ in cursor.get_children():
    child = child_

    # Skip private members
    if child.access_specifier in (cindex.AccessSpecifier.PRIVATE, cindex.AccessSpecifier.PROTECTED):
      continue

    # Skip cursors from included files
    location: cindex.SourceLocation = child.location
    if location.file is None or location.file.name != cursor.translation_unit.spelling:
      continue

    # Namespaces
    if child.kind == cindex.CursorKind.NAMESPACE: next_traverse(child)
    else:
      # Type aliases: if met, unwrap, and continue with the underlying type
      type_alias_cursor = None

      while child.kind in [cindex.CursorKind.TYPE_ALIAS_DECL, cindex.CursorKind.TYPEDEF_DECL]:
        if type_alias_cursor is None: type_alias_cursor = child
        assert child is not None
        underlying_type = child.underlying_typedef_type
        child = underlying_type.get_declaration()

      handled = True
      assert child is not None

      if child.kind == cindex.CursorKind.CXX_METHOD: handled = on_method(child)
      elif child.kind == cindex.CursorKind.PARM_DECL: handled = on_parameter(child)
      elif child.kind == cindex.CursorKind.FIELD_DECL: handled = on_field(child)
      elif child.kind == cindex.CursorKind.CONSTRUCTOR: handled = on_constructor(child)
      elif child.kind == cindex.CursorKind.CXX_BASE_SPECIFIER: handled = on_base_specifier(child)
      elif child.is_definition() or type_alias_cursor:
        if child.kind == cindex.CursorKind.STRUCT_DECL: handled = on_struct(child, type_alias_cursor)
        elif child.kind == cindex.CursorKind.CLASS_DECL: handled = on_class(child, type_alias_cursor)
        elif child.kind == cindex.CursorKind.ENUM_DECL: handled = on_enum(child)
        elif child.kind == cindex.CursorKind.ENUM_CONSTANT_DECL: handled = on_enum_value(child)

      # Continue traversal if not handled
      if not handled: next_traverse(child)


# Get the namespaces of a cursor
def get_cursor_namespaces(cursor: cindex.Cursor) -> list[str]:
  namespaces = []
  parent = cursor.semantic_parent

  while parent and parent.kind in (cindex.CursorKind.NAMESPACE, cindex.CursorKind.STRUCT_DECL, cindex.CursorKind.CLASS_DECL):
    namespaces.append(parent.spelling)
    parent = parent.semantic_parent

  return list(reversed(namespaces))


# Return a default value string for a cursor, if any
def get_default_value(cursor: cindex.Cursor) -> Optional[str]:
  i = 0
  for token in cursor.get_tokens():
    if token.spelling == '=':
      tokens = list(cursor.get_tokens())
      default_value_tokens = tokens[i + 1:]
      default_value = ' '.join(t.spelling for t in default_value_tokens)
      return default_value.strip()

    i += 1
  return None
