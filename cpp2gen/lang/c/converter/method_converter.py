from __future__ import annotations

from typing import Optional

from ._base import CElement
from ..utils import to_c_name
from ....model import Method, Structure, Constructor


class CMethod(Method, CElement):
  base: Method


def convert_method(method: Method) -> Method:
  from . import convert_parameter, convert_type_to_ref_ptr

  params = [convert_parameter(p) for p in method.parameters]
  c_method = CMethod(
    name=to_c_name(method.full_name),
    return_type=convert_type_to_ref_ptr(method.return_type),
    parameters=params,
  )

  if method.index is not None and not isinstance(method, Constructor): c_method.name += f'_{method.index}'

  c_method.base = method
  return c_method


def _internal_generate_method_call(
  method: Method,
  param_names: Optional[list[str]] = None,
  param_names_suffix: Optional[str] = '_',
) -> str:
  param_names_ = param_names
  if param_names_ is None:
    param_names_ = [
      f'{to_c_name(p.name)}{param_names_suffix or ""}' for p in method.parameters
    ]

  return f'{method.name}({", ".join(param_names_)})'


def _cast_return_type_and_impl(method: Method, c_method: Method):
  assert c_method.impl is not None

  # Cast return type
  from .type_converter import _internal_cast_type_to_ref_ptr
  c_method.impl[-1] = _internal_cast_type_to_ref_ptr(method.return_type, c_method.impl[-1])

  # Return statement (if non-void)
  if method.return_type.base_name != 'void': c_method.impl[-1] = f'return {c_method.impl[-1]};'
  else: c_method.impl[-1] = f'{c_method.impl[-1]};'


def convert_structure_method(method: Method) -> Method:
  from . import convert_structure_lite
  from .parameter_converter import internal_generate_parameters_cast_block
  if isinstance(method, CMethod): return method

  struct = method.parent
  assert struct is not None and isinstance(struct, Structure)
  c_struct = convert_structure_lite(struct)

  c_method = convert_method(method)
  inner_parameters = method.parameters.copy()

  if isinstance(method, Constructor):
    c_method.impl = [
      *internal_generate_parameters_cast_block(inner_parameters),
      f'{struct.full_name_cpp_str}{_internal_generate_method_call(method)}',
    ]
  elif method.is_static:
    c_method.impl = [
      *internal_generate_parameters_cast_block(inner_parameters),
      f'{struct.full_name_cpp_str}::{_internal_generate_method_call(method)}',
    ]
  else:
    c_method.parameters.insert(0, c_struct.type_ptr.as_param('instance'))
    c_method.impl = [
      f'auto instance_ = {c_struct.unwrap("instance")};',
      *internal_generate_parameters_cast_block(inner_parameters),
      f'instance_->{_internal_generate_method_call(method)}',
    ]

  if isinstance(method, Constructor):
    c_method.name = f'{c_method.name}create_{method.index}'

  _cast_return_type_and_impl(method, c_method)
  return c_method
