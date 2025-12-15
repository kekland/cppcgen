from __future__ import annotations

from ._generator import GeneratedCode
from ..converter import convert_enum, convert_enum_value
from ....model import Enum, EnumValue
from ....utils import get_logger

logger = get_logger(__name__)


def generate_enum(enum: Enum) -> GeneratedCode:
  logger.debug(f'generating C code for enum: {enum.full_name_cpp_str}')
  c_enum = convert_enum(enum)

  hdr = [[
    f'// C representation of enum {enum.full_name_cpp_str}',
    f'typedef enum {c_enum.name} {{',
    *(f'  {value.name} = {value.value},' for value in c_enum.values),
    f'}} {c_enum.name};',
  ]]

  from . import generate_method_impl
  src_enum_cv_defs: list[list[str]] = []
  src_enum_cv_defs.append(generate_method_impl(c_enum.to_c_method))
  src_enum_cv_defs.append(generate_method_impl(c_enum.from_c_method))

  return GeneratedCode(
    hdr_enum_defs=hdr,
    src_enum_cv_defs=src_enum_cv_defs,
  )
