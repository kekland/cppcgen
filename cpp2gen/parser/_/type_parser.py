from __future__ import annotations

from clang import cindex
from typing import Optional

from ..utils import get_cursor_namespaces
from ...model import Type
from ...utils import get_logger

logger = get_logger(__name__)


def parse_type(type: cindex.Type) -> Type:
  type_ = type

  # Unwrap pointers and references
  if type_.kind in [cindex.TypeKind.POINTER, cindex.TypeKind.LVALUEREFERENCE, cindex.TypeKind.RVALUEREFERENCE]:
    type_ = type_.get_pointee()

  decl_cursor = type_.get_declaration()
  if decl_cursor is not None and decl_cursor.kind == cindex.CursorKind.NO_DECL_FOUND: decl_cursor = None

  # Ignore declarations for std types - those are handled manually.
  # Also, fix accidental std::__1 namespaces.
  namespaces = get_cursor_namespaces(decl_cursor) if decl_cursor else []
  is_std = len(namespaces) > 0 and namespaces[0] == 'std'

  if is_std: decl_cursor = None
  if namespaces[0:2] == ['std', '__1']: namespaces = ['std'] + namespaces[2:]

  base_name = decl_cursor.spelling if decl_cursor else type_.spelling.split('<')[0].strip().split('::')[-1]

  template_args: Optional[list[Type | str]] = None

  # Override template args for some known std types.
  if is_std:
    if base_name == 'string': template_args = []
    elif base_name == 'array':
      length = type_.spelling.split(',')[1].split('>')[0].strip()
      template_args = [
        parse_type(type_.get_template_argument_type(0)),
        length
      ]

  if template_args is None:
    # TODO: this is a hack
    if decl_cursor and decl_cursor.kind == cindex.CursorKind.TYPE_ALIAS_DECL: template_args = []
    else: template_args = [parse_type(type_.get_template_argument_type(i)) for i in range(type_.get_num_template_arguments())]

  result = Type(
    base_name=base_name,
    namespace=namespaces,
    template_args=template_args,
    is_const=type_.is_const_qualified(),
    is_volatile=type_.is_volatile_qualified(),
    is_lvalue_reference=type.kind == cindex.TypeKind.LVALUEREFERENCE,
    is_rvalue_reference=type.kind == cindex.TypeKind.RVALUEREFERENCE,
    is_pointer=type.kind == cindex.TypeKind.POINTER,
    is_function=type_.kind == cindex.TypeKind.FUNCTIONPROTO,
  )

  if result.is_function:
    from ...model import Parameter
    result.function_return_type = parse_type(type_.get_result())
    params = []

    args = type_.argument_types()
    i = 0
    for t in args:
      param_cpp_type = parse_type(t)
      params.append(Parameter(name=f'p{i}', type=param_cpp_type))
      i += 1

    result.function_parameters = params

  decls = []
  decls.append(result)

  # Recursively parse typedef chain
  if decl_cursor:
    decl = decl_cursor
    while decl_cursor.kind in [cindex.CursorKind.TYPEDEF_DECL, cindex.CursorKind.TYPE_ALIAS_DECL]:
      _d = decl_cursor.underlying_typedef_type.get_declaration()
      if _d is None: break
      if _d.get_usr() == decl.get_usr(): break

      decls.append(parse_type(decl_cursor.underlying_typedef_type))
      decl_cursor = _d

  result.typedefs = decls
  return result
