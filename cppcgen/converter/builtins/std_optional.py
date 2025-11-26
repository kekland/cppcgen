from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure


@dataclass
class StdOptionalStructure(BuiltinStructure):
  arg: cpp.Type

  @property
  def cpp_structure_impl(self):
    return cpp.Structure(
      name=f'optional<{self.arg.full_name}>',
      namespace='std',
      c_structure_=self,
    )

  @property
  def template_file_stem(self) -> str: return 'std_optional'

  @property
  def base_name_impl(self) -> str: return f'std_optional_{self.arg.as_c_ptr.base_name.lower()}'

  def modify_template_file(self, lines: list[str]) -> list[str]: return self.modify_template_file_arg1(lines, self.arg)
