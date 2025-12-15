from __future__ import annotations

from .. import utils
from ..model import cpp


def cpp_method_to_c(cpp_method: cpp.Method) -> cpp.Method:
  parameters: list[cpp.Parameter] = []
  for param in cpp_method.parameters:
    parameters.append(param.as_c)

  return cpp.Method(
    name=utils.cpp_name_to_c_name(cpp_method.full_name),
    return_type=cpp_method.return_type.as_c_ref,
    parameters=parameters,
  )
