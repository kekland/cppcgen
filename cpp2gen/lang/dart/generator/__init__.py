from __future__ import annotations

import pathlib
import subprocess
from typing import Any

from .builtin_generator import generate_builtins
from .enum_generator import generate_enum
from .structure_generator import generate_structure
from ....model import Enum, Structure
from ....utils import get_logger, code_list_to_str

logger = get_logger(__name__)

_prelude: str
with open(pathlib.Path(__file__).parent / '_prelude.dart', 'r') as f: _prelude = f.read()
_start_tag = '// - start prelude\n'
_prelude = _prelude[_prelude.find(_start_tag) + len(_start_tag):]


def generate(entity: Any) -> list[str]:
  if isinstance(entity, Enum): return generate_enum(entity)
  elif isinstance(entity, Structure): return generate_structure(entity)
  else:
    logger.warning(f'no generator found for entity type: {type(entity).__name__}')
    return []


def generate_entities(entities: list[Any]) -> list[str]:
  code: list[str] = []

  for entity in entities:
    entity_code = generate(entity)
    code.append(code_list_to_str(entity_code))

  return code


def generate_ffigen(input_file: pathlib.Path, output_file: pathlib.Path):
  ffigen_script_path = pathlib.Path(__file__).parent / '_ffigen.dart'

  logger.info(f'generating Dart FFI bindings using ffigen: {input_file} -> {output_file}')
  subprocess.run([
    ffigen_script_path,
    str(input_file),
    str(output_file),
  ])


def generate_code(
  entities: list[Any],
  ffigen_input_file: pathlib.Path,
  ffigen_output_file: pathlib.Path
) -> str:
  generate_ffigen(ffigen_input_file, ffigen_output_file)
  code: list[list[str]] = []
  
  code.append([_prelude.replace('//ffigen-import', f'import \'{ffigen_output_file.stem}.dart\' as gen_ffi;')])

  for entity_code in generate_entities(entities):
    code.append([entity_code])

  builtin_code = generate_builtins()
  code.append(builtin_code)

  result_code: list[str] = []
  for part in code:
    result_code.extend(part)
    result_code.append('')

  return code_list_to_str(result_code)


__all__ = [
  'generate_enum',
  'generate',
  'generate_entities',
  'generate_ffigen',
  'generate_builtins',
]
