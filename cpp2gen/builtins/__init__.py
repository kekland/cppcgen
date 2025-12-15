from __future__ import annotations

from dataclasses import dataclass, field
from ._model import BuiltinStructure, BuiltinTemplate, BuiltinTemplates
from typing import Callable
from ..model import Structure, Type, Namespace

from .std_string import StdString, StdStringTemplate
from .std_vector import StdVector, StdVectorTemplate
from .std_pair import StdPair, StdPairTemplate
from .std_chrono_steady_clock_duration import StdChronoSteadyClockDuration, StdChronoSteadyClockDurationTemplate
from .std_optional import StdOptional, StdOptionalTemplate
from .std_array import StdArray, StdArrayTemplate
from .std_shared_ptr import StdSharedPtr
from .std_unique_ptr import StdUniquePtr
from .std_function import StdFunction, StdFunctionTemplate

__all__ = [
  'BuiltinStructure',
  'BuiltinTemplate',
  'BuiltinTemplates',
  'maybe_get_builtin_structure',
  '_used_builtins',
  'StdString', 'StdStringTemplate',
  'StdVector', 'StdVectorTemplate',
  'StdPair', 'StdPairTemplate',
  'StdChronoSteadyClockDuration', 'StdChronoSteadyClockDurationTemplate',
  'StdOptional', 'StdOptionalTemplate',
  'StdArray', 'StdArrayTemplate',
  'StdSharedPtr',
  'StdUniquePtr',
  'StdFunction', 'StdFunctionTemplate',
]

_used_builtins: dict[str, BuiltinStructure] = dict()


def maybe_get_builtin_structure(type: Type) -> BuiltinStructure | None:
  result: BuiltinStructure | None = None
  typedef = None
  i = 0

  for t in type.typedefs:
    if i > 0: typedef = type
    i += 1

    if t.namespace and t.namespace[0] == 'std':
      if t.namespace == ['std', 'chrono', 'steady_clock']:
        if t.base_name == 'duration': result = StdChronoSteadyClockDuration()

      if t.base_name == 'string': result = StdString()
      if t.base_name == 'vector': result = StdVector()
      if t.base_name == 'pair': result = StdPair()
      if t.base_name == 'optional': result = StdOptional()
      if t.base_name == 'array': result = StdArray()
      if t.base_name == 'shared_ptr': result = StdSharedPtr()
      if t.base_name == 'unique_ptr': result = StdUniquePtr()
      if t.base_name == 'function': result = StdFunction()

    if result:
      result.type_ = t
      result.typedef = typedef
      result.setup()
      if result.typedef is not None:
        result.name = result.typedef.base.full_name_cpp_str
        result.parent = None
      break

  # Traverse the template args to setup the chain
  if result:
    for arg in result.type_.template_args:  # type: ignore
      if isinstance(arg, Type): maybe_get_builtin_structure(arg)

  if result: _used_builtins[result._unique_name] = result
  return result
