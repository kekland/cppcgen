from __future__ import annotations

from .. import utils
from ..model import cpp, c


def cpp_enum_value_to_c(enum_value: cpp.EnumValue) -> c.EnumValue:
  return c.EnumValue(
    base=enum_value,
  )


def cpp_enum_to_c(enum: cpp.Enum) -> c.Enum:
  return c.Enum(
    base=enum,
  )


def cpp_enum_to_c_fn(enum: cpp.Enum) -> cpp.Method:
  c_enum = enum.as_c

  cases: list[str] = []
  for i in range(len(enum.values)):
    v = enum.values[i]
    cases.append(f'case {v.full_name}: return {c_enum.values[i].name};')

  return cpp.Method(
    name='to_c',
    namespace='enum_cv',
    is_inline=True,
    is_static=True,
    return_type=enum.as_c.type,
    parameters=[enum.type.as_param('value')],
    impl=[
      f'switch (value) {{',
      *(utils.indent(cases)),
      f'  default: std::abort();',
      f'}}',
    ]
  )


def cpp_enum_from_c_fn(enum: cpp.Enum) -> cpp.Method:
  c_enum = enum.as_c

  cases: list[str] = []
  for i in range(len(enum.values)):
    v = enum.values[i]
    cases.append(f'case {c_enum.values[i].name}: return {v.full_name};')

  return cpp.Method(
    name='to_cpp',
    namespace='enum_cv',
    is_inline=True,
    is_static=True,
    return_type=enum.type,
    parameters=[c_enum.type.as_param('value')],
    impl=[
      f'switch (value) {{',
      *(utils.indent(cases)),
      f'  default: std::abort();',
      f'}}',
    ]
  )
