from __future__ import annotations

from clang import cindex
from logging import getLogger
from typing import Optional

from ... import context, parser
from ...model import cpp


_logger = getLogger('type_parser')


def parse_type(type_: cindex.Type) -> cpp.Type:
  base_type = type_
  pointee_type = type_

  if base_type.kind in [cindex.TypeKind.POINTER, cindex.TypeKind.LVALUEREFERENCE, cindex.TypeKind.RVALUEREFERENCE]:
    base_type = base_type.get_pointee()
    pointee_type = base_type

  if base_type.is_const_qualified() or base_type.is_volatile_qualified():
    base_type = base_type.get_canonical()

  # Get the declaration. If the namespace is std, we ignore the declaration.
  decl_cursor = base_type.get_declaration()
  assert decl_cursor is not None
  namespace = parser.utils.get_cursor_namespace(decl_cursor)
  if namespace.startswith('std'): decl_cursor = None
  if namespace == 'std::__1': namespace = 'std'

  base_name = base_type.spelling
  has_template_args = True

  # If declaration is available, use its spelling as the base name.
  # Otherwise, just clean up the base name.
  if decl_cursor and decl_cursor.spelling: base_name = decl_cursor.spelling
  else: base_name = base_name.split('<', 1)[0].strip().split('::')[-1]


  # Override template args for some known types.
  template_args: Optional[list[cpp.Type]] = None
  if namespace == 'std':
    if base_name == 'string': template_args = []
    if base_name == 'array':
      length = type_.spelling.split(',')[1].split('>')[0].strip()
      template_args = [
        parse_type(base_type.get_template_argument_type(0)),
        cpp.Type(base_name=length)
      ]

  if template_args is None:
    template_args = [parse_type(base_type.get_template_argument_type(i)) for i in range(base_type.get_num_template_arguments())]

  t = cpp.Type(
    cindex_type=type_,
    base_name=base_name,
    namespace=namespace,
    is_const=pointee_type.is_const_qualified(),
    is_volatile=pointee_type.is_volatile_qualified(),
    is_lvalue_reference=type_.kind == cindex.TypeKind.LVALUEREFERENCE,
    is_rvalue_reference=type_.kind == cindex.TypeKind.RVALUEREFERENCE,
    is_pointer=type_.kind == cindex.TypeKind.POINTER,
    template_args=template_args,
  )

  _logger.debug(f'Parsed type: {type_.spelling} -> {t.full_name}, base_name={base_name}, namespace={namespace}')
  return t
