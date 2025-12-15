from __future__ import annotations

import re

from ..model import Type


def modify_template_file_arg(lines: list[str], arg: Type, index: int) -> list[str]:
  from ..lang.c.generator.method_generator import _get_ffi_error_default_return
  from ..lang.c.converter.type_converter import convert_type_to_ptr, convert_type_to_ref_ptr, _internal_cast_type_to_cpp, _internal_cast_type_to_ref_ptr, _internal_cast_type_to_ptr, convert_type
  from ..lang.c.utils.string_utils import to_c_name

  from ..lang.dart.converter.type_converter import convert_type_to_dart, _internal_cast_type_to_dart, _internal_cast_type_to_ffi
  from ..lang.dart.generator.type_generator import generate_type

  suf = str(index)

  arg_cpp_pattern = fr'ARG{suf}_CPP'
  arg_c_ptr_pattern = fr'ARG{suf}_C_PTR'
  arg_c_ref_pattern = fr'ARG{suf}_C_REF'
  arg_pattern = fr'ARG{suf}'
  ptr_pattern = fr'CAST{suf}_TO_C_PTR\(([^)]+)\)'
  ref_pattern = fr'CAST{suf}_TO_C_REF\(([^)]+)\)'
  cpp_pattern = fr'CAST{suf}_TO_CPP\(([^)]+)\)'
  arg_ffi_error_return_pattern = fr'ARG{suf}_FFI_ERROR_RETURN'
  arg_cpp_ret = fr'ARG{suf}_CPP_RET'
  arg_cpp_params = fr'ARG{suf}_CPP_PARAMS'
  arg_dart_pattern = fr'ARG{suf}_DART'
  arg_dart_cast_from_ffi_pattern = fr'ARG{suf}_CAST_FROM_FFI\(([^)]+)\)'
  arg_dart_cast_from_ffi_copy_pattern = fr'ARG{suf}_CAST_FROM_FFI_COPY\(([^)]+)\)'
  arg_dart_cast_to_ffi_pattern = fr'ARG{suf}_CAST_TO_FFI\(([^)]+)\)'

  def _c_type_to_str(t: Type) -> str:
    from ..lang.c.generator.type_generator import generate_type as c_generate_type
    return c_generate_type(t)

  out = []
  for l in lines:
    if arg.is_function:
      assert arg.function_return_type is not None
      l = re.sub(arg_cpp_ret, arg.function_return_type.full_name_cpp_str, l)
      l = re.sub(arg_cpp_params, ', '.join([p.type.full_name_cpp_str for p in arg.function_parameters]), l)

    l = re.sub(arg_dart_pattern, generate_type(convert_type_to_dart(arg)), l)
    l = re.sub(arg_dart_cast_from_ffi_copy_pattern, lambda m: _internal_cast_type_to_dart(arg, m.group(1), ref_copy=True), l)
    l = re.sub(arg_dart_cast_from_ffi_pattern, lambda m: _internal_cast_type_to_dart(arg, m.group(1)), l)
    l = re.sub(arg_dart_cast_to_ffi_pattern, lambda m: _internal_cast_type_to_ffi(arg, m.group(1)), l)

    l = re.sub(arg_ffi_error_return_pattern, _get_ffi_error_default_return(convert_type_to_ref_ptr(arg)), l)
    l = re.sub(arg_cpp_pattern, arg.full_name_cpp_str, l)
    l = re.sub(arg_c_ptr_pattern, _c_type_to_str(convert_type_to_ptr(arg)), l)
    l = re.sub(arg_c_ref_pattern, _c_type_to_str(convert_type_to_ref_ptr(arg)), l)
    l = re.sub(arg_pattern, to_c_name(arg.full_name_cpp_str), l)
    l = re.sub(ptr_pattern, lambda m: _internal_cast_type_to_ptr(arg, m.group(1)), l)
    l = re.sub(ref_pattern, lambda m: _internal_cast_type_to_ref_ptr(arg, m.group(1)), l)
    l = re.sub(cpp_pattern, lambda m: _internal_cast_type_to_cpp(arg, m.group(1)), l)

    out.append(l)

  return out
