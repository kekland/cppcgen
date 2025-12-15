from __future__ import annotations

from clang import cindex
from logging import getLogger
from typing import Optional

from ... import context, parser
from ...model import cpp


_logger = getLogger('type_parser')


_usr_cache: dict[str, cpp.Type] = {}


def cindex_decl_cursors(type: cindex.Type) -> list[cindex.Cursor]:
  decls = []
  decl = type.get_declaration()
  if not decl: return decls
  decls.append(decl)
  while decl.kind in [cindex.CursorKind.TYPEDEF_DECL, cindex.CursorKind.TYPE_ALIAS_DECL]:
    _d = decl.underlying_typedef_type.get_declaration()
    if _d.get_usr() == decl.get_usr(): break
    if _d is not None:
      decls.append(_d)
      decl = _d
    else: break
  return decls


def parse_type(type_: cindex.Type) -> cpp.Type:
  base_type = type_
  pointee_type = type_

  if type_.kind in [cindex.TypeKind.POINTER, cindex.TypeKind.LVALUEREFERENCE, cindex.TypeKind.RVALUEREFERENCE]:
    pointee_type = type_.get_pointee()
    base_type = type_.get_pointee()

  decl_cursor = base_type.get_declaration()
  if decl_cursor is not None and decl_cursor.kind == cindex.CursorKind.NO_DECL_FOUND: decl_cursor = None

  usr = decl_cursor.get_usr() if decl_cursor else None
  if usr and usr in _usr_cache: 
    cached = _usr_cache[usr]
    return cpp.Type(
      cindex_type=base_type,
      base_name=cached.base_name,
      namespace=cached.namespace,
      is_const=pointee_type.is_const_qualified(),
      is_volatile=pointee_type.is_volatile_qualified(),
      is_lvalue_reference=type_.kind == cindex.TypeKind.LVALUEREFERENCE,
      is_rvalue_reference=type_.kind == cindex.TypeKind.RVALUEREFERENCE,
      is_pointer=type_.kind == cindex.TypeKind.POINTER,
      is_function=type_.kind == cindex.TypeKind.FUNCTIONPROTO,
      template_args=cached.template_args,
    )


  # Get the declaration. If the namespace is std, we ignore the declaration.
  namespace = parser.utils.get_cursor_namespace(decl_cursor) if decl_cursor else ''
  if namespace.startswith('std'): decl_cursor = None
  if namespace.startswith('std::__1'): namespace = namespace.replace('std::__1', 'std')

  base_name = base_type.spelling
  if decl_cursor: base_name = decl_cursor.spelling
  else: base_name = base_name.split('<', 1)[0].strip().split('::')[-1]

  # Override template args for some known types.
  template_args: Optional[list[cpp.Type]] = None
  if namespace.startswith('std'):
    if base_name == 'string': template_args = []
    if base_name == 'array':
      length = base_type.spelling.split(',')[1].split('>')[0].strip()
      template_args = [
        parse_type(base_type.get_template_argument_type(0)),
        cpp.Type(base_name=length)
      ]

  if template_args is None:
    # TODO: this is a hack
    if decl_cursor and decl_cursor.kind == cindex.CursorKind.TYPE_ALIAS_DECL: template_args = []
    else: template_args = [parse_type(type_.get_template_argument_type(i)) for i in range(type_.get_num_template_arguments())]
    # template_args = [parse_type(type_.get_template_argument_type(i)) for i in range(type_.get_num_template_arguments())]

  t = cpp.Type(
    cindex_type=base_type,
    base_name=base_name,
    namespace=namespace,
    is_const=pointee_type.is_const_qualified(),
    is_volatile=pointee_type.is_volatile_qualified(),
    is_lvalue_reference=type_.kind == cindex.TypeKind.LVALUEREFERENCE,
    is_rvalue_reference=type_.kind == cindex.TypeKind.RVALUEREFERENCE,
    is_pointer=type_.kind == cindex.TypeKind.POINTER,
    is_function=type_.kind == cindex.TypeKind.FUNCTIONPROTO,
    template_args=template_args,
  )

  _logger.debug(f'Parsed type: {type_.spelling} -> {t.full_name}, base_name={base_name}, namespace={namespace} (decl_cursor={decl_cursor is not None})')
  if usr: _usr_cache[usr] = t
  return t
