from __future__ import annotations

from ._generator import GeneratedCode
from .structure_generator import generate_structure
from ....utils import get_logger

_logger = get_logger(__name__)


def generate_builtins() -> GeneratedCode:
  _logger.info('generating used builtins...')

  code = GeneratedCode()

  from ....builtins import _used_builtins
  from ..builtins import get_builtin_template
  structures = _used_builtins.copy()

  for _, struct in structures.items():
    _logger.info(f'builtin used: {struct.full_name_cpp_str} ({struct.typedef.full_name_cpp_str if struct.typedef else None})')
    if struct.is_passthrough_type:
      _logger.debug(f'skipping code generation for passthrough builtin structure: {struct.full_name_cpp_str}')
      continue

    code_ = generate_structure(struct, force_builtin=True)
    code.merge(code_)

    template = get_builtin_template(struct)
    code.merge(template.generate_code())

  return code
