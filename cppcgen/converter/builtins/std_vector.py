from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure


@dataclass
class StdVectorStructure(BuiltinStructure):
  arg: cpp.Type

  def __post_init__(self):
    self.base = cpp.Structure(
      name=f'vector<{self.arg.full_name}>',
      namespace='std',
      c_structure_=self,
    )

  @property
  def template_file_stem(self) -> str: return 'std_vector'

  @property
  def base_name(self) -> str: return f'std_vector_{self.arg.as_c_ptr.base_name.lower()}'

  def modify_template_file(self, lines: list[str]) -> list[str]: return self.modify_template_file_arg1(lines, self.arg)
