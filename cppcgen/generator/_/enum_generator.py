from __future__ import annotations

from logging import getLogger

from ...model import cpp, c
from ..generated_code import GeneratedCode

_logger = getLogger('enum_generator')


def generate_enum(enum: cpp.Enum) -> GeneratedCode:
  c_enum = enum.as_c
  _logger.debug(f'Generating code for enum: {enum.full_name}')

  hdr = [[
    f'// C representation of enum {enum.full_name}',
    f'typedef enum {c_enum.name} {{',
    *(f'  {value.name} = {value.value},' for value in c_enum.values),
    f'}} {c_enum.name};',
  ]]

  src = []
  src.append(enum.to_c_fn.generate_impl())
  src.append(enum.from_c_fn.generate_impl())

  return GeneratedCode(
    hdr_enum_defs=hdr,
    src_enum_cv_defs=src,
  )
