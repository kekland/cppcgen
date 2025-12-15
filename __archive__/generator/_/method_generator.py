from __future__ import annotations

from typing import Optional
from logging import getLogger

from ...model import cpp
from ... import utils

_logger = getLogger('method_generator')


def generate_method_signature(method: cpp.Method) -> str:
  from .. import generate_parameters, generate_type

  params_str = generate_parameters(method.parameters)
  return_str = generate_type(method.return_type)
  qualifiers = ''

  if method.is_static: qualifiers += 'static '
  if method.is_const: qualifiers += ' const'
  if method.is_inline: qualifiers = 'inline ' + qualifiers

  qualifiers = qualifiers.strip()
  is_export = method.parent is None and not method.namespace

  result = f'{return_str} {method.name}({params_str})'
  if qualifiers: result = f'{qualifiers} {result}'
  if is_export: result = f'FFI {result}'

  return result


def generate_method_decl(method: cpp.Method) -> list[str]:
  _logger.debug(f'Generating method declaration for {method.full_name}')

  signature = generate_method_signature(method)
  return [f'{signature};']


def generate_method_impl(method: cpp.Method, impl: Optional[list[str]] = None) -> list[str]:
  _logger.debug(f'Generating method implementation for {method.full_name}')

  impl_ = impl or method.impl
  if impl_ is None:
    _logger.warning(f'No implementation found for method: {method.name}')
    impl_ = ['// TODO: implement']

  signature = generate_method_signature(method)
  is_export = method.parent is None and not method.namespace

  if is_export:
    return [
      f'{signature} {{',
      f'  FFI_FUNCTION_GUARD_BEGIN',
      *(utils.indent(impl_)),
      f'  FFI_FUNCTION_GUARD_END({method.return_type.ffi_error_default_return})',
      f'}}',
    ]
  else:
    return [
      f'{signature} {{',
      *(utils.indent(impl_)),
      f'}}',
    ]


def generate_method_call(
  method: cpp.Method,
  param_names: Optional[list[str]] = None,
  param_names_suffix: Optional[str] = '_',
):
  param_names_ = param_names
  if param_names_ is None:
    param_names_ = [
      f'{p.name}{param_names_suffix or ""}' for p in method.parameters
    ]

  return f'{method.call_name}({", ".join(param_names_)})'
