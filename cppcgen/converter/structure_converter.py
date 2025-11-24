from __future__ import annotations

from .. import utils
from ..model import cpp, c
from .method_converter import cpp_method_to_c
from ..generator import generate_parameters_cast_block, generate_method_call
from .builtins import maybe_get_builtin_structure


def cpp_structure_create_methods(structure: c.Structure) -> list[cpp.Method]:
  result: list[cpp.Method] = []

  index = 0
  for constructor in structure.base.regular_constructors:
    name = f'{structure.base_name}_create_{index}' if len(structure.base.regular_constructors) > 1 else f'{structure.base_name}_create'
    call = constructor.generate_call()
    method = cpp.Method(
      name=name,
      return_type=structure.ref_type,
      parameters=[param.as_c for param in constructor.parameters],
      impl=[
        *generate_parameters_cast_block(constructor.parameters),
        f'return {structure.wrap_ref_type(f"{structure.base.full_name}{call}")};',
      ],
    )

    result.append(method)
    index += 1
  
  return result


def cpp_structure_destroy_method(structure: c.Structure) -> cpp.Method:
  return cpp.Method(
    name=f'{structure.ref_base_name}_destroy',
    return_type=cpp.Type.void(),
    parameters=[structure.ref_type.as_param('instance')],
    impl=[f'delete {structure.unwrap_ref_type("instance")};']
  )


def cpp_structure_unwrap_method(structure: c.Structure) -> cpp.Method:
  unwrap = structure.unwrap_ref_type('instance')
  unwrap = f'{unwrap}->unwrap()'
  unwrap = structure.wrap_type(unwrap)

  return cpp.Method(
    name=f'{structure.ref_base_name}_unwrap',
    return_type=structure.type,
    parameters=[structure.ref_type.as_param('instance')],
    impl=[f'return {unwrap};']
  )


def cpp_structure_fields_to_c(structure: c.Structure) -> list[cpp.Method]:
  result: list[cpp.Method] = []
  fields: list[cpp.Field] = [*structure.base.fields, *structure.base.synthetic_fields]

  for field in fields:
    # getter
    getter_type = field.getter.return_type if field.getter else field.type
    assert getter_type is not None

    call = f'instance_->'
    if field.getter: call += field.getter.generate_call([])
    else: call += field.name

    result.append(cpp.Method(
      name=f'{structure.base_name}_{utils.cpp_name_to_c_name(field.name)}_get',
      return_type=getter_type.as_c_ref,
      parameters=[structure.type.as_param('instance')],
      impl=[
        f'auto instance_ = {structure.unwrap_type("instance")};',
        f'return {getter_type.cast_to_c_ref(call)};',
      ],
    ))

    # setter
    setter_type = field.setter.parameters[0].type if field.setter else field.type
    assert setter_type is not None

    call = f'instance_->'
    if field.setter: call += field.setter.generate_call(['value_'])
    else: call += f'{field.name} = value_'

    result.append(cpp.Method(
      name=f'{structure.base_name}_{utils.cpp_name_to_c_name(field.name)}_set',
      return_type=cpp.Type.void(),
      parameters=[
        structure.type.as_param('instance'),
        setter_type.as_param('value').as_c,
      ],
      impl=[
        f'auto instance_ = {structure.unwrap_type("instance")};',
        *generate_parameters_cast_block([cpp.Parameter(name='value', type=setter_type)]),
        f'{call};',
      ],
    ))

  return result


def cpp_structure_methods_to_c(structure: c.Structure) -> list[cpp.Method]:
  result: list[cpp.Method] = []

  for method in structure.base.instance_methods:
    call = f'instance_->{generate_method_call(method)}'

    impl = [
      f'auto instance_ = {structure.unwrap_type("instance")};',
      *generate_parameters_cast_block(method.parameters),
    ]

    if method.return_type.is_void:
      impl.append(f'{call};')
    else:
      impl.append(f'auto result_ = {call};')
      impl.append(f'return {method.return_type.cast_to_c_ref("result_")};')

    method = cpp.Method(
      name=f'{structure.base_name}_{utils.cpp_name_to_c_name(method.name)}',
      return_type=method.return_type.as_c_ref,
      parameters=[
        structure.type.as_param('instance'),
        *[param.as_c for param in method.parameters],
      ],
      impl=impl,
    )

    result.append(method)

  return result


def cpp_structure_to_c(cpp_structure: cpp.Structure) -> c.Structure:
  builtin = maybe_get_builtin_structure(cpp_structure.type)
  if builtin is not None: return builtin

  return c.Structure(base=cpp_structure)
