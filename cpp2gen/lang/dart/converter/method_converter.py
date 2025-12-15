from __future__ import annotations

from typing import Optional

from ..utils import to_dart_member_name
from ....model import Method, Structure, Constructor
from ....utils import indent


def convert_method(method: Method) -> Method:
  from . import convert_parameter, convert_type_to_dart

  dart_method = Method(
    name=to_dart_member_name(method.name),
    return_type=convert_type_to_dart(method.return_type),
    parameters=[convert_parameter(p) for p in method.parameters],
  )

  if method.index is not None: dart_method.name += f'{method.index}'
  return dart_method



def convert_method_ffi(method: Method) -> Method:
  from . import convert_parameter_ffi, convert_type_to_ffi_ref_ptr

  name = to_dart_member_name(method.name)
  if isinstance(method, Constructor): name = f'create{method.index}'

  dart_method = Method(
    name=name,
    return_type=convert_type_to_ffi_ref_ptr(method.return_type),
    parameters=[convert_parameter_ffi(p) for p in method.parameters],
  )

  if method.index is not None and not isinstance(method, Constructor): dart_method.name += f'{method.index}'
  return dart_method


def _internal_generate_method_call(
  method: Method,
  param_names: Optional[list[str]] = None,
  param_names_suffix: Optional[str] = '_',
) -> str:
  param_names_ = param_names
  if param_names_ is None:
    param_names_ = [
      f'{to_dart_member_name(p.name)}{param_names_suffix or ""}' for p in method.parameters
    ]

  if method.is_getter: return f'{method.name}'
  if method.is_setter: return f'{method.name} = {param_names_[0]}'

  return f'{method.name}({", ".join(param_names_)})'


def convert_structure_method_ext(method: Method) -> Method:
  from ...c import converter as c_converter
  c_method = c_converter.convert_structure_method(method)
  dart_method = convert_method_ffi(method)

  call = _internal_generate_method_call(c_method, param_names_suffix='')
  call = call.replace('instance', 'this')

  # Method implementation
  dart_method.impl = [f'_ffiCall(() => gen_ffi.{call})']

  dart_method.is_inline = True
  dart_method.is_static = method.is_static
  return dart_method


def convert_structure_method_ext_to_ref_ext(ext_method: Method) -> Method:
  if ext_method.is_static: return ext_method
  return Method(
    name=ext_method.name,
    return_type=ext_method.return_type,
    parameters=ext_method.parameters,
    is_inline=ext_method.is_inline,
    is_static=ext_method.is_static,
    is_getter=ext_method.is_getter,
    is_setter=ext_method.is_setter,
    impl=[
      f'unwrap().{_internal_generate_method_call(ext_method, param_names_suffix="")}'
    ]
  )


def convert_structure_method(method: Method) -> Method:
  from ...c import converter as c_converter
  from ...c.converter._base import CElement
  from .parameter_converter import convert_parameter, internal_generate_parameters_cast_block
  from .type_converter import convert_type_to_dart, _internal_cast_type_to_dart

  parameters = [convert_parameter(p) for p in method.parameters]
  ext_method = convert_structure_method_ext(method)

  ptr = 'ptr'
  if method.is_static:
    c_struct: Structure
    if isinstance(method, CElement): c_struct = method.parameters[0].type.decl_repr  # type: ignore
    else: c_struct = c_converter.convert_structure_lite(method.parent)  # type: ignore
    ptr = f'{c_struct.name}_ref_ext'

  impl = [
    *internal_generate_parameters_cast_block(method.parameters),
    f'final result = {ptr}.{_internal_generate_method_call(ext_method)};',
    f'return {_internal_cast_type_to_dart(method.return_type, "result")};',
  ]

  _cls: type[Method]
  name: str

  if isinstance(method, Constructor):
    _cls = Constructor
    name = f'create{method.index}'
  else:
    _cls = Method
    name = to_dart_member_name(method.name)
    if method.index is not None: name += f'{method.index}'

  impl = indent(impl)
  impl = [
    f'return using((arena) {{',
    *impl,  # type: ignore
    f'}});',
  ]

  return _cls(
    name=name,
    return_type=convert_type_to_dart(method.return_type),
    parameters=parameters,
    impl=impl,
    is_static=method.is_static,
  )


def convert_structure_constructor(ctor: Method | Constructor) -> Constructor:
  m = convert_structure_method(ctor)  # type: ignore
  if isinstance(m, Constructor): return m

  return Constructor(
    name=m.name,
    return_type=m.return_type,
    parameters=m.parameters,
    impl=m.impl,
    is_static=m.is_static,
  )
