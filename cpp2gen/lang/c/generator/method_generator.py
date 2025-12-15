from __future__ import annotations

from typing import Optional

from ._generator import GeneratedCode
from ....model import Method, Enum, Type
from ....utils import get_logger, indent

_logger = get_logger('method_generator')


def _get_ffi_error_default_return(type: Type) -> str:
  if type.base_name == 'void': return ''

  decl_repr = type.decl_repr
  if isinstance(decl_repr, Enum): return decl_repr.values[0].name

  return '0'


def generate_method_signature(method: Method) -> str:
  from . import generate_parameters, generate_type

  params_str = generate_parameters(method.parameters)
  return_str = generate_type(method.return_type)
  qualifiers = ''

  if method.is_static: qualifiers += 'static '
  if method.is_const: qualifiers += ' const'
  if method.is_inline: qualifiers = 'inline ' + qualifiers

  qualifiers = qualifiers.strip()
  is_export = method.parent is None

  result = f'{return_str} {method.name}({params_str})'
  if qualifiers: result = f'{qualifiers} {result}'
  if is_export: result = f'FFI {result}'

  return result


def generate_method_decl(method: Method) -> list[str]:
  _logger.debug(f'Generating method declaration for {method.name}')

  signature = generate_method_signature(method)
  return [f'{signature};']


def generate_method_impl(method: Method, impl: Optional[list[str]] = None) -> list[str]:
  _logger.debug(f'Generating method implementation for {method.name}')

  impl_ = impl or method.impl
  if impl_ is None:
    _logger.warning(f'No implementation found for method: {method.name}')
    impl_ = ['// TODO: implement']

  signature = generate_method_signature(method)
  is_export = method.parent is None

  if is_export:
    return [
      f'{signature} {{',
      f'  FFI_FUNCTION_GUARD_BEGIN',
      *(indent(impl_)),
      f'  FFI_FUNCTION_GUARD_END({_get_ffi_error_default_return(method.return_type)})',
      f'}}',
    ]
  else:
    return [
      f'{signature} {{',
      *(indent(impl_)),
      f'}}',
    ]


def generate_method(method: Method) -> GeneratedCode:
  hdr = generate_method_decl(method)
  src = generate_method_impl(method)

  return GeneratedCode(
    hdr=[hdr],
    src=[src],
  )
