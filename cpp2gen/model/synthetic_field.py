from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .type import Type
from .method import Method
from .field import Field


@dataclass
# A semantic representation of a synthetic field/member variable which is represented by a pair of getter/setter methods.
class SyntheticField(Field):
  getter: Optional[Method] = field(default=None)
  setter: Optional[Method] = field(default=None)
  type: Optional[Type] = field(init=False, default=None)
