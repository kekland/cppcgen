from __future__ import annotations

import pathlib
from logging import getLogger

_logger = getLogger('builtin_generator')


def generate_builtins() -> list[str]:
  from ...converter.builtins import _used_builtins
  structures = _used_builtins

  for name, structure in structures.items():
    _logger.info(f'Builtin used: {name}')
    if structure.is_passthrough_type:
      _logger.debug(f'Skipping code generation for passthrough builtin structure: {structure.base.full_name}')
      continue

  return code
