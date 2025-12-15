from __future__ import annotations

from dataclasses import dataclass, field

from ._model import BuiltinStructure, BuiltinTemplate
from ..model import Container, Namespace, Type


@dataclass
class StdString(BuiltinStructure):
  name: str = field(default='string', init=False)
  parent: Container | None = field(default_factory=lambda: Namespace('std'), init=False)


@dataclass
class StdStringTemplate(BuiltinTemplate):
  @property
  def base_name_impl(self) -> str: return 'std_string'
