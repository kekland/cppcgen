from __future__ import annotations

from typing import Any

from ..model import Element


def _element_to_dict(element: Element) -> dict:
  result: dict[str, Any] = {
    'type': type(element).__name__,
  }

  for k, v in element.__repr_attrs__().items():
    r = v

    if isinstance(v, Element): r = _element_to_dict(v)
    elif isinstance(v, list):
      r = []
      for item in v:
        if isinstance(item, Element): r.append(_element_to_dict(item))
        else: r.append(item)

    result[k] = r

  return result


def dump_element(element: Element, indent: int = 2) -> str:
  import json
  element_dict = _element_to_dict(element)
  return json.dumps(element_dict, indent=indent,default=lambda o: o.toJSON() if hasattr(o, 'toJSON') else str(o))
