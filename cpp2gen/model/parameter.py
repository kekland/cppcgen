from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .element import Element
from .type import Type


@dataclass
# A semantic representation of a parameter of a method/function/constructor/etc.
class Parameter(Element):
  type: Type
  default_value: Optional[str] = None  # literal for a default value, if any
  is_name_synthetic: bool = False  # set to True for unnamed parameters: name will be 'p{index}'

  def __repr_keys__(self): return ['type', 'name', 'default_value', 'is_name_synthetic']
