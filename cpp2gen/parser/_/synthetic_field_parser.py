from __future__ import annotations

from clang import cindex
from typing import Optional

from .method_parser import parse_method
from ..utils import traverse_cursor
from ...model import Namespace, Container, Element, Structure, Method, SyntheticField, Field, Constructor
from ...utils import get_logger, uncapitalize, cpp_name_to_c_name, c_name_to_cpp_name

logger = get_logger(__name__)


def _potential_synthetic_field_setter_name(method: Method) -> str | None:
  if len(method.parameters) != 1: return None
  if method.name.startswith('set') and len(method.name) > 3: return uncapitalize(cpp_name_to_c_name(method.name[3:]))
  if method.name.startswith('with') and len(method.name) > 4: return uncapitalize(cpp_name_to_c_name(method.name[4:]))
  return None


def _potential_synthetic_field_getter_name(method: Method) -> str | None:
  if len(method.parameters) != 0: return None
  if method.name.startswith('get') and len(method.name) > 3: return uncapitalize(cpp_name_to_c_name(method.name[3:]))
  return None


def _find_potential_synthetic_getter_for_setter(setter: Method, methods: list[Method]) -> Optional[Method]:
  field_name = _potential_synthetic_field_setter_name(setter)
  if field_name is None: return None

  for method in methods:
    if method is setter: continue
    getter_field_name = _potential_synthetic_field_getter_name(method)
    if getter_field_name == field_name or cpp_name_to_c_name(method.name) == field_name: return method

  return None


def _find_potential_synthetic_setter_for_getter(getter: Method, methods: list[Method]) -> Optional[Method]:
  field_name = _potential_synthetic_field_getter_name(getter)
  if field_name is None: return None

  for method in methods:
    if method is getter: continue
    setter_field_name = _potential_synthetic_field_setter_name(method)
    if setter_field_name == field_name: return method

  return None


def filter_children_for_synthetic_fields(parent: Container, children: list[Element]) -> tuple[list[Element], list[SyntheticField]]:
  synthetic_fields: list[SyntheticField] = []
  used_method_names: set[str] = set()
  used_field_names: set[str] = set()
  methods = [c for c in children if isinstance(c, Method) and not isinstance(c, Constructor) and not c.is_static]
  fields = [c for c in children if isinstance(c, Field)]

  def find_field(name: str) -> Optional[Field]:
    for field in fields:
      if field.name == name: return field
      if field.name == c_name_to_cpp_name(name): return field
    return None

  for method in methods:
    if method.name in used_method_names: continue
    setter_field_name = _potential_synthetic_field_setter_name(method)
    getter_field_name = _potential_synthetic_field_getter_name(method)

    if setter_field_name is not None:
      used_method_names.add(method.name)
      getter = _find_potential_synthetic_getter_for_setter(method, methods)
      if getter is not None: used_method_names.add(getter.name)

      logger.debug(f'parsed synthetic field: {setter_field_name} from setter method: {method.name} (getter: {getter.name if getter else "None"})')
      field = find_field(setter_field_name)
      if field: used_field_names.add(field.name)

      synthetic_fields.append(
        SyntheticField(
          name=field.name if field else setter_field_name,
          setter=method,
          getter=getter,
          parent=parent,
          type=field.type if field else None,
        )
      )
    elif getter_field_name is not None:
      used_method_names.add(method.name)
      setter = _find_potential_synthetic_setter_for_getter(method, methods)
      if setter is not None: used_method_names.add(setter.name)

      logger.debug(f'parsed synthetic field: {getter_field_name} from getter method: {method.name} (setter: {setter.name if setter else "None"})')
      field = find_field(getter_field_name)
      if field: used_field_names.add(field.name)

      synthetic_fields.append(
        SyntheticField(
          name=field.name if field else getter_field_name,
          setter=setter,
          getter=method,
          parent=parent,
          type=field.type if field else None,
        )
      )

  filtered_children = [c for c in children if not (isinstance(c, Method) and c.name in used_method_names)]
  filtered_children = [c for c in filtered_children if not (isinstance(c, Field) and c.name in used_field_names)]
  return filtered_children, synthetic_fields
