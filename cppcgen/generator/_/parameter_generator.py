from __future__ import annotations

from logging import getLogger

from ...model import cpp

_logger = getLogger('parameter_generator')


def generate_parameter(parameter: cpp.Parameter) -> str:
  return f'{parameter.type.full_name} {parameter.name}'


def generate_parameters(parameters: list[cpp.Parameter]) -> str:
  return ', '.join(generate_parameter(p) for p in parameters)


def generate_parameters_cast_block(parameters: list[cpp.Parameter], parameter_suffix: str = '_') -> list[str]:
  lines: list[str] = []

  for p in parameters:
    lines.append(f'{p.type.full_name} {p.name}{parameter_suffix} = {p.type.as_c_ptr.cast_to_cpp(p.name)};')

  return lines
