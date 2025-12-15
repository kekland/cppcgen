from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
from ..model import Structure, Type, Namespace


@dataclass
class BuiltinStructure(Structure):
  typedef: Type | None = field(default=None, init=False)

  def setup(self) -> None: pass

  @property
  def is_passthrough_type(self) -> bool: return self.passthrough_type is not None

  @property
  def passthrough_type(self) -> Type | None: return None

  @property
  def _unique_name(self) -> str:
    if self.typedef is not None: return self.typedef.base.full_name_cpp_str
    return self.name


@dataclass
class BuiltinTemplate:
  structure: BuiltinStructure = field()

  @property
  def should_generate(self) -> bool: return True

  @property
  def type_(self) -> Type: return self.structure.type_ # type: ignore

  @property
  def typedef(self) -> Type | None: return self.structure.typedef

  @property
  def base_name_impl(self) -> str: raise NotImplementedError()

  @property
  def base_name(self) -> str:
    from ..lang.c.utils.string_utils import to_c_name
    if self.typedef is not None: return to_c_name(self.typedef.full_name_cpp_str)
    return self.base_name_impl

  @property
  def template_file_stem(self) -> str | None: return self.base_name_impl

  def replace_base_name(self, lines: list[str]) -> list[str]:
    out = []
    for l in lines:
      l = l.replace('BASE_NAME', self.base_name)
      l = l.replace(self.base_name_impl, self.base_name)
      out.append(l)
    return out

  def modify_template_file(self, lines: list[str]) -> list[str]: return lines


@dataclass
class BuiltinTemplates:
  std_string: Callable[[BuiltinStructure], BuiltinTemplate]
  std_vector: Callable[[BuiltinStructure], BuiltinTemplate]
  std_pair: Callable[[BuiltinStructure], BuiltinTemplate]
  std_chrono_steady_clock_duration: Callable[[BuiltinStructure], BuiltinTemplate]
  std_optional: Callable[[BuiltinStructure], BuiltinTemplate]
  std_array: Callable[[BuiltinStructure], BuiltinTemplate]
  std_function: Callable[[BuiltinStructure], BuiltinTemplate]

  def match(self, structure: BuiltinStructure) -> BuiltinTemplate:
    from .std_string import StdString
    from .std_vector import StdVector
    from .std_pair import StdPair
    from .std_chrono_steady_clock_duration import StdChronoSteadyClockDuration
    from .std_optional import StdOptional
    from .std_array import StdArray
    from .std_function import StdFunction

    if isinstance(structure, StdString): return self.std_string(structure)
    if isinstance(structure, StdVector): return self.std_vector(structure)
    if isinstance(structure, StdPair): return self.std_pair(structure)
    if isinstance(structure, StdChronoSteadyClockDuration): return self.std_chrono_steady_clock_duration(structure)
    if isinstance(structure, StdOptional): return self.std_optional(structure)
    if isinstance(structure, StdArray): return self.std_array(structure)
    if isinstance(structure, StdFunction): return self.std_function(structure)

    raise ValueError(f'no builtin template for structure: {structure.full_name_cpp_str}')
