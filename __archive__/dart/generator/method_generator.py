from typing import Optional

from ...dart import model as dart
from .parameter_generator import generate_parameters

from ... import utils


def generate_method_signature(method: dart.Method) -> str:
  return_type = method.return_type
  parameters = method.parameters
  name = method.name

  param_signature = generate_parameters(parameters)

  if method.is_getter:
    if parameters: raise ValueError('Getter methods cannot have parameters')
    return f'{return_type.name} get {name}'
  elif method.is_setter:
    if len(parameters) != 1: raise ValueError('Setter methods must have exactly one parameter')
    return f'set {name}({param_signature})'

  return f'{return_type.name} {name}({param_signature})'


def generate_method_decl(method: dart.Method) -> list[str]:
  code: list[str] = []
  signature = generate_method_signature(method)
  code.append(f'{signature};')
  return code


def generate_method_impl(method: dart.Method, impl: Optional[list[str]] = None) -> list[str]:
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
      code.extend(utils.indent(impl_))
      code.append('}')

  return code
