from __future__ import annotations

from dataclasses import dataclass, field

from ._model import BuiltinStructure, BuiltinTemplate
from ..model import Container, Namespace, Type
from ._utils import modify_template_file_arg


@dataclass
class StdUniquePtr(BuiltinStructure):
  name: str = field(default='unique_ptr', init=False)
  parent: Container | None = field(default_factory=lambda: Namespace('std'), init=False)

  def setup(self) -> None: self.name = f'unique_ptr<{self.arg.full_name_cpp_str}>'

  @property
  def arg(self) -> Type: return self.type_.template_args[0]  # type: ignore

  @property
  def passthrough_type(self) -> Type: return self.arg
