from __future__ import annotations

from ....model import Enum
from ....utils import indent, get_logger

logger = get_logger(__name__)

def generate_enum(e: Enum) -> list[str]:
  from ...c import converter as c_converter
  from .. import converter as dart_converter
  from .method_generator import generate_method_impl
  logger.debug(f'generating Dart code for enum: {e.full_name_cpp_str}')

  code: list[str] = []
  c_enum = c_converter.convert_enum(e)
  dart_enum = dart_converter.convert_enum(e)

  # Enum declaration
  code.append(f'// Representation of {e.full_name_cpp_str}')
  code.append(f'enum {e.name} {{')

  i = 0
  for i in range(len(dart_enum.values)):
    value = dart_enum.values[i]
    is_last = i == len(e.values) - 1
    d = ',' if not is_last else ';'
    code.append(f'  {value.name}({value.value}){d}')
    i += 1

  code.append(f'')

  # Constructor and value field
  code.append(f'  const {e.name}(this.value);')
  code.append(f'  final int value;')

  # fromFfi/toFfi methods
  code.append(f'')
  code.extend(indent(generate_method_impl(dart_enum.from_ffi_method)))
  code.append(f'')
  code.extend(indent(generate_method_impl(dart_enum.to_ffi_method)))

  code.append(f'}}')

  return code
