from __future__ import annotations

from dataclasses import dataclass, field

from ._model import BuiltinStructure, BuiltinTemplate
from ..model import Container, Namespace, Type
from ._utils import modify_template_file_arg
from ..lang.c.utils.string_utils import to_c_name


@dataclass
class StdOptional(BuiltinStructure):
  name: str = field(default='optional', init=False)
  parent: Container | None = field(default_factory=lambda: Namespace('std'), init=False)

  def setup(self) -> None: self.name = f'optional<{self.arg.full_name_cpp_str}>'

  @property
  def arg(self) -> Type: return self.type_.template_args[0]  # type: ignore


@dataclass
class StdOptionalTemplate(BuiltinTemplate):
  @property
  def arg(self) -> Type: return self.type_.template_args[0]  # type: ignore

  @property
  def template_file_stem(self) -> str: return 'std_optional'

  @property
  def base_name_impl(self) -> str: return f'std_optional_{to_c_name(self.arg.full_name_cpp_str).lower()}'

  def modify_template_file(self, lines: list[str]) -> list[str]:
    lines = modify_template_file_arg(lines, self.arg, 1)
    return lines
