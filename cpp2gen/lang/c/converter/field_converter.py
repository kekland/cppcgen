from __future__ import annotations

from typing import Optional

from .method_converter import CMethod
from ..utils import to_c_name
from ....model import Field, Method, Structure, Type


def convert_field(field: Field) -> tuple[Optional[Method], Optional[Method]]:
  from .method_converter import _internal_generate_method_call
  from .type_converter import convert_type_to_ref_ptr, convert_type_to_ptr, _internal_cast_type_to_ref_ptr, _internal_cast_type_to_cpp
  from .structure_converter import convert_structure_lite

  struct = field.parent
  assert struct is not None and isinstance(struct, Structure)
  c_struct = convert_structure_lite(struct)

  field_name = field.name
  getter: Optional[Method] = None
  setter: Optional[Method] = None

  getter_type = field.getter.return_type if field.getter else field.type
  setter_type = field.setter.parameters[0].type if field.setter else field.type

  if getter_type is not None:
    call = f'instance_->'
    if field.getter: call += _internal_generate_method_call(field.getter)
    else: call += field.name

    getter = CMethod(
      name=to_c_name([*struct.full_name, field_name, 'get']),
      return_type=convert_type_to_ref_ptr(getter_type),
      parameters=[c_struct.type_ptr.as_param('instance')],
      impl=[
        f'auto instance_ = {c_struct.unwrap("instance")};',
        f'return {_internal_cast_type_to_ref_ptr(getter_type, call)};',
      ]
    )

  if setter_type is not None:
    call = f'instance_->'
    if field.setter: call += _internal_generate_method_call(field.setter, param_names=['value_'])
    else:
      from ....builtins import StdOptional
      if isinstance(setter_type.decl_repr, StdOptional): call = f'if (value_.has_value()) {{ instance_->{field.name}.emplace(value_.value()); }} else {{ instance_->{field.name}.reset(); }}'
      else: call += f'{field.name} = value_'

    setter = CMethod(
      name=to_c_name([*struct.full_name, field_name, 'set']),
      return_type=Type.void(),
      parameters=[
        c_struct.type_ptr.as_param('instance'),
        convert_type_to_ptr(setter_type).as_param('value'),
      ],
      impl=[
        f'auto instance_ = {c_struct.unwrap("instance")};',
        f'auto value_ = {_internal_cast_type_to_cpp(setter_type, "value")};',
        f'{call};',
      ]
    )

  return getter, setter
