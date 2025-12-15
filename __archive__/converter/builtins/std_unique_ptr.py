from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure


@dataclass
class StdUniquePtrStructure(BuiltinStructure):
  arg: cpp.Type

  @property
  def cpp_structure_impl(self):
    return cpp.Structure(
      name=f'unique_ptr<{self.arg.full_name}>',
      namespace='std',
      c_structure_=self,
    )

  @property
  def is_passthrough_type(self) -> bool: return True

  @property
  def template_file_stem(self) -> str | None: return None

  @property
  def base_name_impl(self) -> str: return f'std_unique_ptr_{self.arg.as_c_ptr.base_name.lower()}'

  def modify_template_file(self, lines: list[str]) -> list[str]: return self.modify_template_file_arg1(lines, self.arg)

  def unwrap_ref_type(self, var_name: str) -> str: return self.arg.as_structure.as_c.unwrap_ref_type(var_name)
  def unwrap_type(self, var_name: str) -> str: return self.arg.as_structure.as_c.unwrap_type(var_name)

  def wrap_ref_type(self, var_name: str) -> str: return self.arg.as_structure.as_c.wrap_ref_type(f'std::move({var_name})')
  def wrap_type(self, var_name: str) -> str: return self.arg.as_structure.as_c.wrap_type(f'std::move({var_name})')
