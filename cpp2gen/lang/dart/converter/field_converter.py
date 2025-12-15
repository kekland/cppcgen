from __future__ import annotations

from typing import Optional

from ..utils import to_dart_member_name
from ....model import Field, Method, Structure, Type


def convert_field(field: Field) -> tuple[Optional[Method], Optional[Method]]:
  from .method_converter import _internal_generate_method_call
  from .parameter_converter import convert_parameter
  from .type_converter import convert_type_to_dart, _internal_cast_type_to_dart, _internal_cast_type_to_ffi
  ext_getter, ext_setter = convert_field_ext(field)

  getter: Optional[Method] = None
  if ext_getter:
    original_type = field.getter.return_type if field.getter else field.type  # type: ignore
    assert original_type is not None

    dart_type = convert_type_to_dart(original_type)

    call = f'ptr.{_internal_generate_method_call(ext_getter)}'
    call = _internal_cast_type_to_dart(original_type, call)

    getter = Method(
      name=ext_getter.name,
      return_type=dart_type,
      parameters=[],
      is_getter=True,
      impl=[f'return using((arena) => {call});']
    )

  setter: Optional[Method] = None
  if ext_setter:
    original_type = field.setter.parameters[0].type if field.setter else field.type  # type: ignore
    assert original_type is not None

    dart_type = convert_type_to_dart(original_type)

    param = ext_setter.parameters[0]
    call = _internal_cast_type_to_ffi(original_type, param.name)
    call = f'ptr.{_internal_generate_method_call(ext_setter, param_names=[f"{call}"])}'

    setter = Method(
      name=ext_setter.name,
      return_type=Type(base_name='void'),
      parameters=[dart_type.as_param(param.name)],
      is_setter=True,
      impl=[f'using((arena) => {call});'],
    )

  return (getter, setter)


def convert_field_ext(field: Field) -> tuple[Optional[Method], Optional[Method]]:
  from .method_converter import convert_structure_method_ext
  from ...c import converter as c_converter

  c_getter, c_setter = c_converter.convert_field(field)

  dart_getter, dart_setter = (
    convert_structure_method_ext(c_getter) if c_getter else None,
    convert_structure_method_ext(c_setter) if c_setter else None,
  )

  if dart_getter:
    dart_getter.name = to_dart_member_name(field.name)
    dart_getter.parameters.pop(0)
    dart_getter.is_getter = True
  if dart_setter:
    dart_setter.name = to_dart_member_name(field.name)
    dart_setter.parameters.pop(0)
    dart_setter.is_setter = True

  return (dart_getter, dart_setter)
