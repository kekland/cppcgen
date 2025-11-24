from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure


@dataclass
class StdStringStructure(BuiltinStructure):
  def __post_init__(self):
    self.base = cpp.Structure(
      name='string',
      namespace='std',
    )

  @property
  def base_name(self) -> str: return 'std_string'
