from __future__ import annotations

from dataclasses import dataclass, field

from ._model import BuiltinStructure, BuiltinTemplate
from ..model import Container, Namespace, Type
from ._utils import modify_template_file_arg


@dataclass
class StdPair(BuiltinStructure):
  name: str = field(default='pair', init=False)
  parent: Container | None = field(default_factory=lambda: Namespace('std'), init=False)

  def setup(self) -> None: self.name = f'pair<{self.arg1.full_name_cpp_str}, {self.arg2.full_name_cpp_str}>'

  @property
  def arg1(self) -> Type: return self.type_.template_args[0]  # type: ignore

  @property
  def arg2(self) -> Type: return self.type_.template_args[1]  # type: ignore


@dataclass
class StdPairTemplate(BuiltinTemplate):
  @property
  def arg1(self) -> Type: return self.type_.template_args[0]  # type: ignore

  @property
  def arg2(self) -> Type: return self.type_.template_args[1]  # type: ignore

  @property
  def template_file_stem(self) -> str: return 'std_pair'

  @property
  def base_name_impl(self) -> str: return f'std_pair_{self.arg1.base_name.lower()}_{self.arg2.base_name.lower()}'

  def modify_template_file(self, lines: list[str]) -> list[str]:
    lines = modify_template_file_arg(lines, self.arg1, 1)
    lines = modify_template_file_arg(lines, self.arg2, 2)
    return lines
