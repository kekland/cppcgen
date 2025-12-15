from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ...model import cpp, c
from ..builtins import BuiltinStructure


@dataclass
class StdChronoSteadyClockDurationStructure(BuiltinStructure):
  @property
  def cpp_structure_impl(self):
    return cpp.Structure(
      name='steady_clock::duration',
      namespace='std::chrono',
    )

  @property
  def base_name_impl(self) -> str: return 'std_chrono_steady_clock_duration'
