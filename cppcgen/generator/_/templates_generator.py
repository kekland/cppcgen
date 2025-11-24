from __future__ import annotations

import pathlib
from logging import getLogger
from ..generated_code import GeneratedCode, generate_divider

_logger = getLogger('helpers_generator')


def generate_templates() -> GeneratedCode:
  _logger.info('Generating templates...')
  src_helpers = []
  src_helpers.extend(generate_divider(['Templates for ffi_cv and ref']))

  with open(pathlib.Path(__file__).parent / 'templates.hpp', 'r') as f:
    for l in f.readlines(): src_helpers.append(l.rstrip())

  return GeneratedCode(
    src_struct_defs=[src_helpers]
  )
