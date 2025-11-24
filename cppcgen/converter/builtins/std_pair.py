from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure


@dataclass
class StdPairStructure(BuiltinStructure):
  arg1: cpp.Type
  arg2: cpp.Type

  def __post_init__(self):
    self.base = cpp.Structure(
      name=f'pair<{self.arg1.full_name}, {self.arg2.full_name}>',
      namespace='std',
      c_structure_=self,
    )

  @property
  def template_file_stem(self) -> str: return 'std_pair'

  @property
  def base_name(self) -> str: return f'std_pair_{self.arg1.as_c_ptr.base_name.lower()}_{self.arg2.as_c_ptr.base_name.lower()}'

  def modify_template_file(self, lines: list[str]) -> list[str]:
    lines = self.modify_template_file_arg1(lines, self.arg1)
    lines = self.modify_template_file_arg2(lines, self.arg2)
    return lines