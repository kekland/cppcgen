from __future__ import annotations

from clang import cindex
from logging import getLogger

from ... import context, parser, utils
from ...model import cpp

_logger = getLogger('synthetic_field_parser')


def _potential_synthetic_field_setter_name(method: cpp.Method) -> str | None:
  if len(method.parameters) != 1: return None
  if method.name.startswith('set') and len(method.name) > 3: return utils.uncapitalize(utils.cpp_name_to_c_name(method.name[3:]))
  if method.name.startswith('with') and len(method.name) > 4: return utils.uncapitalize(utils.cpp_name_to_c_name(method.name[4:]))
  return None


def _potential_synthetic_field_getter_name(method: cpp.Method) -> str | None:
  if len(method.parameters) != 0: return None
  if method.name.startswith('get') and len(method.name) > 3: return utils.uncapitalize(utils.cpp_name_to_c_name(method.name[3:]))
  return None


def _find_potential_synthetic_getter_for_setter(setter: cpp.Method, methods: list[cpp.Method]) -> cpp.Method | None:
  field_name = _potential_synthetic_field_setter_name(setter)
  if field_name is None: return None

  for method in methods:
    if method is setter: continue
    getter_field_name = _potential_synthetic_field_getter_name(method)
    if getter_field_name == field_name or utils.cpp_name_to_c_name(method.name)== field_name: return method

  return None


def _find_potential_synthetic_setter_for_getter(getter: cpp.Method, methods: list[cpp.Method]) -> cpp.Method | None:
  field_name = _potential_synthetic_field_getter_name(getter)
  if field_name is None: return None

  for method in methods:
    if method is getter: continue
    setter_field_name = _potential_synthetic_field_setter_name(method)
    if setter_field_name == field_name: return method

  return None


def filter_methods_for_synthetic_fields(parent: cpp.Structure, methods: list[cpp.Method]) -> tuple[list[cpp.Method], list[cpp.SyntheticField]]:
  synthetic_fields: list[cpp.SyntheticField] = []
  used_method_names: set[str] = set()

  for method in methods:
    if method.name in used_method_names: continue
    setter_field_name = _potential_synthetic_field_setter_name(method)
    getter_field_name = _potential_synthetic_field_getter_name(method)

    if setter_field_name is not None:
      used_method_names.add(method.name)
      getter = _find_potential_synthetic_getter_for_setter(method, methods)
      if getter is not None: used_method_names.add(getter.name)

      _logger.debug(f'Parsed synthetic field: {setter_field_name} from setter method: {method.name} (getter: {getter.name if getter else "None"})')

      synthetic_fields.append(
        cpp.SyntheticField(
          name=setter_field_name,
          setter=method,
          getter=getter,
          parent_=parent,
        )
      )
    elif getter_field_name is not None:
      used_method_names.add(method.name)
      setter = _find_potential_synthetic_setter_for_getter(method, methods)
      if setter is not None: used_method_names.add(setter.name)

      _logger.debug(f'Parsed synthetic field: {getter_field_name} from getter method: {method.name} (setter: {setter.name if setter else "None"})')

      synthetic_fields.append(
        cpp.SyntheticField(
          name=getter_field_name,
          setter=setter,
          getter=method,
          parent_=parent,
        )
      )

  filtered_methods = [m for m in methods if m.name not in used_method_names]
  return filtered_methods, synthetic_fields
