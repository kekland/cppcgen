from __future__ import annotations

from ._generator import GeneratedCode
from ..converter import convert_structure
from ....model import Structure
from ....utils import get_logger
from ....builtins import BuiltinStructure, maybe_get_builtin_structure

logger = get_logger(__name__)


def generate_structure(struct: Structure, force_builtin=False) -> GeneratedCode:
  if not force_builtin and maybe_get_builtin_structure(struct.type) is not None: return GeneratedCode()

  logger.debug(f'generating C code for structure: {struct.full_name_cpp_str}')
  c_struct = convert_structure(struct)

  # Structure typedefs
  hdr_struct_defs = [
    f'// Opaque pointers and typedefs for ref<{struct.full_name_cpp_str}>',
    f'struct {c_struct.ref.name};',
    f'typedef struct {c_struct.ref.name}* {c_struct.ref.ptr_typedef_name};',
    '',
    f'// Opaque pointers and typedefs for {struct.full_name_cpp_str}',
    f'struct {c_struct.name};',
    f'typedef struct {c_struct.name}* {c_struct.ptr_typedef_name};',
  ]

  if isinstance(struct, BuiltinStructure):
    type = (struct.typedef or struct.type_)
    assert type is not None

    src_struct_defs = [
      f'// Typedef helpers for {type.full_name_cpp_str}',
      f'struct {c_struct.ref.name} : public ffi_cv<{c_struct.ref.name}, ref<{type.base.full_name_cpp_str}>> {{}};',
      f'struct {c_struct.name} : public ffi_cv<{c_struct.name}, {type.base.full_name_cpp_str}> {{}};',
    ]
  else:
    src_struct_defs = [
      f'// Typedef helpers for {struct.full_name_cpp_str}',
      f'struct {c_struct.ref.name} : public ffi_cv<{c_struct.ref.name}, ref<{struct.full_name_cpp_str}>> {{}};',
      f'struct {c_struct.name} : public ffi_cv<{c_struct.name}, {struct.full_name_cpp_str}> {{}};',
    ]

  # Structure code
  hdr: list[list[str]] = [[]]
  src: list[list[str]] = []

  for child in c_struct.children:
    from . import generate

    child_code = generate(child)
    hdr[-1].extend(child_code.hdr[0])
    src.extend(child_code.src)

  return GeneratedCode(
    hdr_struct_defs=[hdr_struct_defs],
    src_struct_defs=[src_struct_defs],
    hdr=hdr,
    src=src,
  )
