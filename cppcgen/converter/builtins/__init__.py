from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field

from ...model import cpp, c
from ...generator import GeneratedCode
from ... import utils

import pathlib
import re


_used_builtins: dict[str, BuiltinStructure] = {}


def maybe_get_builtin_structure(type: cpp.Type) -> Optional[BuiltinStructure]:
  from .std_string import StdStringStructure
  from .std_vector import StdVectorStructure
  from .std_optional import StdOptionalStructure
  from .std_array import StdArrayStructure
  from .std_pair import StdPairStructure
  from .std_chrono_steady_clock_duration import StdChronoSteadyClockDurationStructure

  result: Optional[BuiltinStructure] = None

  typedef_name = None
  i = 0
  for t in type.decl_typedefs:
    name = t.namespaced_base_name
    if i > 0: typedef_name = type.namespaced_base_name
    i += 1

    if name == 'std::string': result = StdStringStructure(typedef_name=typedef_name)
    elif name == 'std::vector': result = StdVectorStructure(arg=t.template_args[0], typedef_name=typedef_name)
    elif name == 'std::optional': result = StdOptionalStructure(arg=t.template_args[0], typedef_name=typedef_name)
    elif name == 'std::array': result = StdArrayStructure(arg=t.template_args[0], size=int(t.template_args[1].base_name), typedef_name=typedef_name)
    elif name == 'std::pair': result = StdPairStructure(arg1=t.template_args[0], arg2=t.template_args[1], typedef_name=typedef_name)
    elif name == 'std::chrono::steady_clock::duration': result = StdChronoSteadyClockDurationStructure(typedef_name=typedef_name)

    if result is not None: break

  if result is not None: _used_builtins[result.base_name_impl] = result
  return result


def get_builtin_structure(type: cpp.Type) -> c.Structure:
  builtin = maybe_get_builtin_structure(type)
  if builtin is None: raise ValueError(f'Type {type.full_name} is not a recognized builtin structure')
  return builtin


def modify_template_file_arg(lines: list[str], arg: cpp.Type, index: int) -> list[str]:
  suf = str(index)

  arg_cpp_pattern = fr'ARG{suf}_CPP'
  arg_c_ptr_pattern = fr'ARG{suf}_C_PTR'
  arg_c_ref_pattern = fr'ARG{suf}_C_REF'
  arg_pattern = fr'ARG{suf}'
  ptr_pattern = fr'CAST{suf}_TO_C_PTR\(([^)]+)\)'
  ref_pattern = fr'CAST{suf}_TO_C_REF\(([^)]+)\)'
  cpp_pattern = fr'CAST{suf}_TO_CPP\(([^)]+)\)'
  arg_ffi_error_return_pattern = fr'ARG{suf}_FFI_ERROR_RETURN'

  out = []
  for l in lines:
    l = re.sub(arg_ffi_error_return_pattern, arg.ffi_error_default_return, l)
    l = re.sub(arg_cpp_pattern, arg.full_name, l)
    l = re.sub(arg_c_ptr_pattern, arg.as_c_ptr.full_name, l)
    l = re.sub(arg_c_ref_pattern, arg.as_c_ref.full_name, l)
    l = re.sub(arg_pattern, arg.as_c_ptr.base_name.lower(), l)
    l = re.sub(ptr_pattern, lambda m: arg.cast_to_c_ptr(m.group(1)), l)
    l = re.sub(ref_pattern, lambda m: arg.cast_to_c_ref(m.group(1)), l)
    l = re.sub(cpp_pattern, lambda m: arg.cast_to_cpp(m.group(1)), l)
    out.append(l)

  return out


@dataclass
class BuiltinStructure(c.Structure):
  base: cpp.Structure = field(init=False)
  typedef_name: Optional[str] = field()

  @property
  def base_name_impl(self) -> str: raise NotImplementedError()

  @property
  def cpp_structure_impl(self) -> cpp.Structure: raise NotImplementedError()

  @property
  def base_name(self) -> str:
    if self.typedef_name is not None: return utils.cpp_name_to_c_name(self.typedef_name)
    return self.base_name_impl

  def __post_init__(self):
    if self.typedef_name is not None:
      self.base = cpp.Structure(
        name=self.typedef_name,
        namespace='',
        c_structure_=self,
      )
    else:
      self.base = self.cpp_structure_impl

  @property
  def template_file_stem(self) -> str: return self.base_name_impl

  def modify_template_file(self, lines: list[str]) -> list[str]: return lines

  def modify_template_file_arg1(self, lines: list[str], arg1: cpp.Type) -> list[str]: return modify_template_file_arg(lines, arg1, 1)
  def modify_template_file_arg2(self, lines: list[str], arg2: cpp.Type) -> list[str]: return modify_template_file_arg(lines, arg2, 2)

  def replace_base_name(self, lines: list[str]) -> list[str]:
    out = []
    for l in lines:
      l = re.sub(fr'{self.base_name_impl}', self.base_name, l)
      out.append(l)
    return out

  @property
  def template_code(self) -> GeneratedCode:
    file_name = pathlib.Path(__file__).parent / f'{self.template_file_stem}.hpp'
    with open(file_name, 'r') as f: content = f.read().splitlines()
    content = self.modify_template_file(content)
    content = self.replace_base_name(content)

    code = GeneratedCode()
    hdr_start_index = content.index('// -- hdr') + 1
    hdr_end_index = content.index('// -- src')
    src_start_index = hdr_end_index + 1
    src_end_index = len(content)

    code.hdr = [content[hdr_start_index:hdr_end_index]]
    code.src = [content[src_start_index:src_end_index]]

    return code

  @property
  def create_methods(self) -> list[cpp.Method]:
    return []

  @property
  def field_methods(self) -> list[cpp.Method]:
    return []

  @property
  def methods(self) -> list[cpp.Method]:
    return []
