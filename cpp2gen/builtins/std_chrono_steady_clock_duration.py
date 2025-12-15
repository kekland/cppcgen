from __future__ import annotations

from dataclasses import dataclass, field

from ._model import BuiltinStructure, BuiltinTemplate
from ..model import Container, Namespace, Type


@dataclass
class StdChronoSteadyClockDuration(BuiltinStructure):
  name: str = field(default='duration', init=False)
  parent: Container | None = field(default_factory=lambda: Namespace('steady_clock', parent=Namespace('chrono', parent=Namespace('std'))), init=False)


@dataclass
class StdChronoSteadyClockDurationTemplate(BuiltinTemplate):
  @property
  def base_name_impl(self) -> str: return 'std_chrono_steady_clock_duration'
