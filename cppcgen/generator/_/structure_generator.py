from __future__ import annotations

from logging import getLogger

from ...model import cpp, c
from ..generated_code import GeneratedCode

_logger = getLogger('structure_generator')


def _generate_structure_typedefs(structure: c.Structure) -> GeneratedCode:
  hdr = [
    f'// Opaque pointers and typedefs for {structure.base.full_name} (ref)',
    f'struct {structure.ref_base_name};',
    f'typedef {structure.ref_base_name}* {structure.ref_name};',
    '',
    f'// Opaque pointers and typedefs for {structure.base.full_name} (ptr)',
    f'struct {structure.base_name};',
    f'typedef {structure.base_name}* {structure.name};',
  ]

  src = [
    f'// Typedef helpers for {structure.base.full_name}',
    f'struct {structure.ref_base_name} : public ffi_cv<{structure.ref_base_name}, ref<{structure.base.full_name}>> {{}};',
    f'struct {structure.base_name} : public ffi_cv<{structure.base_name}, {structure.base.full_name}> {{}};',
  ]

  return GeneratedCode(
    hdr_struct_defs=[hdr],
    src_struct_defs=[src],
  )


def generate_structure(structure: cpp.Structure | c.Structure) -> GeneratedCode:
  full_name = structure.full_name if isinstance(structure, cpp.Structure) else structure.base_name
  _logger.debug(f'Generating code for structure: {full_name}')
  if structure.type.is_builtin_structure:
    _logger.debug(f'Skipping code generation for builtin structure: {full_name}')
    return GeneratedCode()

  hdr = []
  src = []

  c_structure = structure.as_c if isinstance(structure, cpp.Structure) else structure

  for method in c_structure.all_methods:
    hdr.extend(method.generate_decl())
    src.append(method.generate_impl())

  code = GeneratedCode(
    hdr=[hdr],
    src=src,
  )

  code.merge(_generate_structure_typedefs(c_structure))
  return code
