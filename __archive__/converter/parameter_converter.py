from __future__ import annotations

from .. import utils
from ..model import cpp

from .type_converter import cpp_type_to_c_ptr

def cpp_parameter_to_c(cpp_parameter: cpp.Parameter) -> cpp.Parameter:
  return cpp.Parameter(
    type=cpp_type_to_c_ptr(cpp_parameter.type),
    name=utils.cpp_name_to_c_name(cpp_parameter.name),
  )
