from __future__ import annotations

from typing import Optional

from ....model import Method, Constructor
from ....utils import indent


def generate_method_signature(method: Method) -> str:
  return_type = method.return_type
  parameters = method.parameters
  name = method.name

  from .parameter_generator import generate_parameters
  from .type_generator import generate_type
  param_signature = generate_parameters(parameters)
  return_type_str = generate_type(return_type)
  qualifiers = ''

  if isinstance(method, Constructor):
    return f'factory {return_type_str}.{name}({param_signature})'

  if method.is_inline: qualifiers += '@_inline '
  if method.is_static: qualifiers += 'static '

  if method.is_getter:
    if parameters: raise ValueError('Getter methods cannot have parameters')
    return f'{qualifiers}{return_type_str} get {name}'
  elif method.is_setter:
    if len(parameters) != 1: raise ValueError('Setter methods must have exactly one parameter')
    return f'{qualifiers}set {name}({param_signature})'

  return f'{qualifiers}{return_type_str} {name}({param_signature})'


def generate_method_decl(method: Method) -> list[str]:
  code: list[str] = []
  signature = generate_method_signature(method)
  code.append(f'{signature};')
  return code


def generate_method_impl(method: Method, impl: Optional[list[str]] = None) -> list[str]:
  code: list[str] = []
  signature = generate_method_signature(method)

  code.append(f'{signature}')
  impl_ = impl or method.impl

  if not impl_:
    code[-1] += ' {'
    code.append('  // TODO: Implement method')
    code.append('}')
  else:
    if len(impl_) == 1:
      line = impl_[0]
      if line.startswith('return '): line = line[len('return '):]
      line = line.strip()
      line = line.rstrip(';')
      code[-1] += f' => {line};'
    else:
      code[-1] += ' {'
      code.extend(indent(impl_))
      code.append('}')

  return code
