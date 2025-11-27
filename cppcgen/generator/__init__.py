from .generated_code import GeneratedCode, generate_divider
from ._.builtin_generator import generate_builtins
from ._.enum_generator import generate_enum
from ._.templates_generator import generate_templates
from ._.method_generator import generate_method_signature, generate_method_decl, generate_method_impl, generate_method_call
from ._.parameter_generator import generate_parameter, generate_parameters, generate_parameters_cast_block
from ._.includes_generator import generate_includes
from ._.structure_generator import generate_structure
from ._.type_generator import generate_type, generate_type_cast_to_c_ref, generate_type_cast_to_cpp, generate_type_cast_to_c_ptr

from typing import Union, Optional
from logging import getLogger
from ..model import cpp

_logger = getLogger('generator')


def _generate(entity) -> Optional[GeneratedCode]:
  _logger.info(f'Generating code for entity: {entity.full_name}')
  if isinstance(entity, cpp.Structure): return generate_structure(entity)
  if isinstance(entity, cpp.Enum): return generate_enum(entity)
  _logger.warning(f'No generator for entity type {type(entity)}: {entity.name}')
  return None


def generate(entity) -> GeneratedCode:
  code = _generate(entity)
  if code is None: return GeneratedCode()

  divider = generate_divider([f'Generated code for entity: {entity.name}'])

  # Prepend dividers
  if code.hdr: code.hdr.insert(0, divider)
  if code.src: code.src.insert(0, divider)

  return code


__all__ = [
  'GeneratedCode',
  'generate_builtins',
  'generate_enum',
  'generate_divider',
  'generate_templates',
  'generate_includes',
  'generate_structure',
  'generate_type',
  'generate_type_cast_to_c_ref',
  'generate_type_cast_to_c_ptr',
  'generate_type_cast_to_cpp',
  'generate_parameter',
  'generate_parameters',
  'generate_parameters_cast_block',
  'generate_method_signature',
  'generate_method_decl',
  'generate_method_impl',
  'generate_method_call',
  'generate',
]
