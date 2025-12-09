from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .type import Type


@dataclass
# A semantic representation of a parameter of a method/function/constructor/etc.
class Parameter:
  type: Type
  name: str
  default_value: Optional[str] = None  # literal for a default value, if any
  is_name_synthetic: bool = False  # set to True for unnamed parameters: name will be 'p{index}'
