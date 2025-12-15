from __future__ import annotations

from ._base import DartElement
from ..utils import to_dart_member_name
from ....model import Parameter


class DartParameter(Parameter, DartElement):
  base: Parameter


def convert_parameter(parameter: Parameter) -> Parameter:
  from .type_converter import convert_type_to_dart

  p = DartParameter(
    name=to_dart_member_name(parameter.name),
    type=convert_type_to_dart(parameter.type),
    is_name_synthetic=parameter.is_name_synthetic,
  )

  p.base = parameter
  return p


def convert_parameter_ffi(parameter: Parameter) -> Parameter:
  from .type_converter import convert_type_to_ffi_ptr

  p = DartParameter(
    name=to_dart_member_name(parameter.name),
    type=convert_type_to_ffi_ptr(parameter.type),
    is_name_synthetic=parameter.is_name_synthetic,
  )

  p.base = parameter
  return p


def internal_generate_parameters_cast_block(parameters: list[Parameter], parameter_suffix: str = '_') -> list[str]:
  lines: list[str] = []
  inner_parameters: list[Parameter] = []

  from .type_converter import _internal_cast_type_to_ffi

  if all(isinstance(p, DartParameter) for p in parameters): inner_parameters = [p.base for p in parameters]  # type: ignore
  else: inner_parameters = parameters

  for i in range(len(parameters)):
    cpp_param = inner_parameters[i]
    param_name = to_dart_member_name(cpp_param.name)
    name = f'{param_name}{parameter_suffix}'
    cast = _internal_cast_type_to_ffi(cpp_param.type, param_name)

    lines.append(f'final {name} = {cast};')

  return lines
