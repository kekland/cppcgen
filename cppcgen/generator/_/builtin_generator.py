from __future__ import annotations

import pathlib
from logging import getLogger
from ..generated_code import GeneratedCode, generate_divider
from .structure_generator import generate_structure

_logger = getLogger('builtin_generator')


def generate_builtins() -> GeneratedCode:
  _logger.info('Generating used builtins...')

  code = GeneratedCode()

  from ...converter.builtins import _used_builtins
  structures = _used_builtins

  for name, structure in structures.items():
    _logger.info(f'Builtin used: {name}')
    code_ = generate_structure(structure)

    divider = generate_divider([f'Built-in structure: {structure.base.full_name}'])
    code.hdr.append(divider)
    code.src.append(divider)

    code.merge(code_)

    template_code = structure.template_code
    code.merge(template_code)

  return code
