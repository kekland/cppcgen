from ...dart import model as dart


def generate_parameters_cast_block(parameters: list[dart.Parameter]) -> list[str]:
  code: list[str] = []

  for param in parameters:
    code.append(f'final {param.name}_ = {param.name};')

  return code


def generate_parameters(parameters: list[dart.Parameter]) -> str:
  code: str = ''

  for param in parameters:
    is_last = param == parameters[-1]
    d = '' if is_last else ', '
    code += f'{param.type.name} {param.name}{d}'

  return code
