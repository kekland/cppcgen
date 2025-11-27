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
    if getter_type is not None:
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
    if setter_type is not None:
      call = f'instance_->'
      if field.setter: call += field.setter.generate_call(['value_'])
      else:
        if setter_type.is_std_optional:
          call = f'if (value_.has_value()) {{ instance_->{field.name}.emplace(value_.value()); }} else {{ instance_->{field.name}.reset(); }}'
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
  method_name_counts: dict[str, int] = {}

  for method in structure.base.instance_methods:
    # Ignore operator methods
    if method.is_operator: continue
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

    # Ensure unique method names
    name = f'{structure.base_name}_{utils.cpp_name_to_c_name(method.name)}'
    if name in method_name_counts:
      method_name_counts[name] += 1
      name = f'{name}_{method_name_counts[name]}'
    elif len(structure.base.find_methods_by_name(method.name)) > 1:
      method_name_counts[name] = 1
      name = f'{name}_1'

    method = cpp.Method(
      name=name,
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
