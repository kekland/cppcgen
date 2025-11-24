# Parser context holds global state for the parsing process.

from __future__ import annotations

from typing import Any, Optional
from .model import cpp

_parsed_structures: dict[str, cpp.Structure] = {}
_parsed_enums: dict[str, cpp.Enum] = {}


def _find_by_usr(usr: str, d: dict[str, Any]) -> Optional[Any]: return d.get(usr, None)


def _find_by_full_name(full_name: str, d: dict[str, Any]) -> Optional[Any]:
  for i in d.values():
    if i.full_name == full_name: return i
  return None


def _add_entity(d: dict[str, Any], e: Any): d[e.cindex_usr] = e


def _find_structure_by_usr(usr: str) -> Optional[cpp.Structure]: return _find_by_usr(usr, _parsed_structures)
def _find_structure_by_full_name(full_name: str) -> Optional[cpp.Structure]: return _find_by_full_name(full_name, _parsed_structures)
def _find_enum_by_usr(usr: str) -> Optional[cpp.Enum]: return _find_by_usr(usr, _parsed_enums)
def _find_enum_by_full_name(full_name: str) -> Optional[cpp.Enum]: return _find_by_full_name(full_name, _parsed_enums)


def add_structure(s: cpp.Structure): _add_entity(_parsed_structures, s)
def has_structure(full_name: str) -> bool: return _find_structure_by_full_name(full_name) is not None
def has_structure_by_usr(usr: str) -> bool: return _find_structure_by_usr(usr) is not None
def get_structure(full_name: str) -> Optional[cpp.Structure]: return _find_structure_by_full_name(full_name)
def get_structure_by_usr(usr: str) -> Optional[cpp.Structure]: return _find_structure_by_usr(usr)


def add_enum(e: cpp.Enum): _add_entity(_parsed_enums, e)
def has_enum(full_name: str) -> bool: return _find_enum_by_full_name(full_name) is not None
def has_enum_by_usr(usr: str) -> bool: return _find_enum_by_usr(usr) is not None
def get_enum(full_name: str) -> Optional[cpp.Enum]: return _find_enum_by_full_name(full_name)
def get_enum_by_usr(usr: str) -> Optional[cpp.Enum]: return _find_enum_by_usr(usr)


def has_entity(full_name: str) -> bool: return has_structure(full_name) or has_enum(full_name)
def has_entity_by_usr(usr: str) -> bool: return has_structure_by_usr(usr) or has_enum_by_usr(usr)
def get_entity(full_name: str) -> Optional[cpp.Structure | cpp.Enum]: return get_structure(full_name) or get_enum(full_name)
def get_entity_by_usr(usr: str) -> Optional[cpp.Structure | cpp.Enum]: return get_structure_by_usr(usr) or get_enum_by_usr(usr)


def clear():
  _parsed_structures.clear()
  _parsed_enums.clear()
