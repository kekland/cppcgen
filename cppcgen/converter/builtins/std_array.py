from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure


@dataclass
class StdArrayStructure(BuiltinStructure):
  arg: cpp.Type
  size: int

  def __post_init__(self):
    self.base = cpp.Structure(
      name=f'array<{self.arg.full_name}, {self.size}>',
      namespace='std',
      c_structure_=self,
    )

  @property
  def template_file_stem(self) -> str: return 'std_array'

  @property
  def base_name(self) -> str: return f'std_array_{self.arg.as_c_ptr.base_name.lower()}_{self.size}'

  def modify_template_file(self, lines: list[str]) -> list[str]:
    lines = self.modify_template_file_arg1(lines, self.arg)

    out = []
    for l in lines:
      l = l.replace('SIZE', str(self.size))
      out.append(l)

    return out
