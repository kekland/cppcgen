from __future__ import annotations

from ._base import CElement
from ..utils import to_c_name
from ....model import Parameter


class CParameter(Parameter, CElement):
  base: Parameter


def convert_parameter(parameter: Parameter) -> Parameter:
  from .type_converter import convert_type_to_ptr

  p = CParameter(
    name=to_c_name(parameter.name),
    type=convert_type_to_ptr(parameter.type),
    is_name_synthetic=parameter.is_name_synthetic,
  )

  p.base = parameter
  return p


def internal_generate_parameters_cast_block(parameters: list[Parameter], parameter_suffix: str = '_') -> list[str]:
  lines: list[str] = []
  inner_parameters: list[Parameter] = []

  from .type_converter import _internal_cast_type_to_cpp

  if all(isinstance(p, CParameter) for p in parameters): inner_parameters = [p.base for p in parameters]  # type: ignore
  else: inner_parameters = parameters

  for i in range(len(parameters)):
    cpp_param = inner_parameters[i]
    p = parameters[i]
    param_name = to_c_name(p.name)

    cpp_type = cpp_param.type.full_name_cpp_str
    name = f'{param_name}{parameter_suffix}'
    cast = _internal_cast_type_to_cpp(p.type, param_name)

    lines.append(f'{cpp_type} {name} = {cast};')

  return lines
