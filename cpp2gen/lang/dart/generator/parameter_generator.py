from __future__ import annotations


from ....model import Parameter
from ....utils import get_logger

logger = get_logger(__name__)


def generate_parameter(parameter: Parameter) -> str:
  from .type_generator import generate_type
  return f'{generate_type(parameter.type)} {parameter.name}'


def generate_parameters(parameters: list[Parameter]) -> str:
  return ', '.join(generate_parameter(p) for p in parameters)


def generate_parameters_cast_block(parameters: list[Parameter], parameter_suffix: str = '_') -> list[str]:
  lines: list[str] = []

  for p in parameters:
    lines.append('')
    # lines.append(f'{p.type.full_name} {p.name}{parameter_suffix} = {p.type.as_c_ptr.cast_to_cpp(utils.cpp_name_to_c_name(p.name))};')

  return lines
