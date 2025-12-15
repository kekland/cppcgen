from __future__ import annotations

from .structure_generator import generate_structure
from ..utils import to_dart_top_level_name
from ....utils import get_logger

_logger = get_logger(__name__)


def generate_builtins() -> list[str]:
  _logger.info('generating used builtins...')

  code: list[str] = []

  from ....builtins import _used_builtins
  from ..builtins import get_builtin_template, maybe_convert_type_to_builtin
  from .type_generator import generate_type
  structures = _used_builtins.copy()
  

  for _, struct in structures.items():
    _logger.info(f'builtin used: {struct.full_name_cpp_str} ({struct.typedef.full_name_cpp_str if struct.typedef else None})')
    if struct.is_passthrough_type:
      _logger.debug(f'skipping code generation for passthrough builtin structure: {struct.full_name_cpp_str}')
      continue

    # Add typedef if present
    if struct.typedef:
      dart_name = to_dart_top_level_name(struct.typedef.base.base_name)
      dart_type = generate_type(maybe_convert_type_to_builtin(struct.type, resolve_typedef=False)) # type:ignore
      code.append(f'typedef {dart_name} = {dart_type};')

    # Generate template code
    template = get_builtin_template(struct)
    code.extend(template.generate_code())

  return code
