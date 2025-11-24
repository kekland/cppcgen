from __future__ import annotations

import pathlib
from logging import getLogger
from ..generated_code import GeneratedCode

_logger = getLogger('includes_generator')


def generate_includes(
  include_dirs: list[pathlib.Path],
  files_to_parse: list[pathlib.Path],
  output_hdr_file: pathlib.Path,
  output_src_file: pathlib.Path,
) -> GeneratedCode:
  _logger.debug('Generating includes...')

  # For each file, try to find the include path, and generate the appropriate include directive.
  hdr_includes: list[str] = []
  src_includes: list[str] = []

  for file_path in files_to_parse:
    include_path = None
    for include_dir in include_dirs:
      try:
        relative_path = file_path.relative_to(include_dir)
        include_path = relative_path.as_posix()
        break
      except ValueError:
        continue

    if include_path is None:
      _logger.warning(f'Could not determine include path for file: {file_path}, skipping include generation.')
      continue

    src_includes.append(f'<{include_path}>')

  src_includes.append(f'<cstdint>')
  src_includes.append(f'<memory>')
  src_includes.append(f'<string>')
  src_includes.append(f'<vector>')

  hdr_includes.append(f'"stdint.h"')

  return GeneratedCode(
    hdr_includes=set(hdr_includes),
    src_includes=set(src_includes),
  )
