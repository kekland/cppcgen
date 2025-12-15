from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure
from ... import utils


@dataclass
class StdFunctionStructure(BuiltinStructure):
  arg: cpp.Type

  @property
  def cpp_structure_impl(self):
    return cpp.Structure(
      name=f'function<{self.arg.full_name}>',
      namespace='std',
      c_structure_=self,
    )

  @property
  def return_type(self) -> cpp.Type: return self.arg.function_return_type

  @property
  def argument_types(self) -> list[cpp.Type]: return list(map(lambda x: x.type, self.arg.function_parameters))

  @property
  def fn_type_name(self) -> str:
    return f'{utils.cpp_name_to_c_name(self.return_type.full_name.lower())}$' + '_'.join(map(lambda x: utils.cpp_name_to_c_name(x.full_name).lower(), self.argument_types))

  @property
  def template_file_stem(self) -> str: return 'std_function'

  @property
  def base_name_impl(self) -> str: return f'std_function_{self.fn_type_name}'

  def modify_template_file(self, lines: list[str]) -> list[str]: return self.modify_template_file_arg1(lines, self.arg)
