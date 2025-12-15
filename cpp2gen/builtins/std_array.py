from __future__ import annotations

from dataclasses import dataclass, field

from ._model import BuiltinStructure, BuiltinTemplate
from ..model import Container, Namespace, Type
from ._utils import modify_template_file_arg


@dataclass
class StdArray(BuiltinStructure):
  name: str = field(default='array', init=False)
  parent: Container | None = field(default_factory=lambda: Namespace('std'), init=False)

  def setup(self) -> None: self.name = f'array<{self.arg.full_name_cpp_str}, {self.size}>'

  @property
  def arg(self) -> Type: return self.type_.template_args[0]  # type: ignore

  @property
  def size(self) -> int: return int(self.type_.template_args[1])  # type: ignore


@dataclass
class StdArrayTemplate(BuiltinTemplate):
  @property
  def arg(self) -> Type: return self.type_.template_args[0]  # type: ignore

  @property
  def size(self) -> int: return int(self.type_.template_args[1])  # type: ignore

  @property
  def template_file_stem(self) -> str: return 'std_array'

  @property
  def base_name_impl(self) -> str: return f'std_array_{self.arg.base_name.lower()}_{self.size}'

  def modify_template_file(self, lines: list[str]) -> list[str]:
    lines = [line.replace('SIZE', str(self.size)) for line in lines]
    lines = modify_template_file_arg(lines, self.arg, 1)
    return lines
