from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure


@dataclass
class StdStringStructure(BuiltinStructure):
  @property
  def cpp_structure_impl(self):
    return cpp.Structure(
      name='string',
      namespace='std',
    )

  @property
  def base_name_impl(self) -> str: return 'std_string'
