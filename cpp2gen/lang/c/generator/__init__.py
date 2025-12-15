from __future__ import annotations

import pathlib
from typing import Any

from ._generator import GeneratedCode
from .builtin_generator import generate_builtins
from .enum_generator import generate_enum
from .parameter_generator import generate_parameter, generate_parameters, generate_parameters_cast_block
from .method_generator import generate_method_decl, generate_method_impl, generate_method_signature, generate_method
from .includes_generator import generate_includes
from .structure_generator import generate_structure
from .type_generator import generate_type

from ....model import Enum, Structure, Method
from ....utils import get_logger

logger = get_logger(__name__)


def generate(entity: Any) -> GeneratedCode:
  if isinstance(entity, Enum): return generate_enum(entity)
  elif isinstance(entity, Structure): return generate_structure(entity)
  elif isinstance(entity, Method): return generate_method(entity)
  else:
    logger.warning(f'no generator found for entity type: {type(entity).__name__}')
    return GeneratedCode()


def generate_entities(entities: list[Any]) -> GeneratedCode:
  code = GeneratedCode()

  for entity in entities:
    entity_code = generate(entity)
    code.merge(entity_code)

  return code


def generate_code(
  entities: list[Any],
  include_dirs: list[pathlib.Path],
  files_to_parse: list[pathlib.Path],
  output_hdr_file: pathlib.Path,
  output_src_file: pathlib.Path,
) -> tuple[str, str]:
  code = GeneratedCode()

  # Prepare includes
  code.merge(generate_includes(include_dirs=include_dirs, files_to_parse=files_to_parse))

  # Generate entities
  code.merge(generate_entities(entities))
  
  # Generate builtins
  code.merge(generate_builtins())

  hdr_code, src_code = code.finalize()

  # Append hdr include to src
  src_code = f'#include "{output_hdr_file.name}"\n\n' + src_code
  return (hdr_code, src_code)


__all__ = [
  'generate',
  'generate_entities',
  'generate_builtins',
  'generate_enum',
  'generate_parameter',
  'generate_parameters',
  'generate_parameters_cast_block',
  'generate_method_signature',
  'generate_method_decl',
  'generate_method_impl',
  'generate_method',
  'generate_structure',
  'generate_type',
]
