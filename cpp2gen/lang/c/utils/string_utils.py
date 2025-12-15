from functools import singledispatch
from typing import Union


# Convert a string to a C-compatible name (lower_case_with_underscores)
@singledispatch
def to_c_name(s: Union[str, list[str]]) -> str: raise NotImplementedError()


@to_c_name.register(str)
def _(s: str) -> str:
  result = []

  s = s.replace('ID', 'Id')
  s = s.replace('URL', 'Url')
  s = s.replace('HTTP', 'Http')
  s = s.replace('HTTPS', 'Https')
  s = s.replace('JSON', 'Json')
  s = s.replace('::', '_')
  s = s.replace(', ', ',')

  for i, char in enumerate(s):
    if char.isupper():
      if i != 0 and result[-1] != '_': result.append('_')
      result.append(char.lower())
    elif char == ' ' or char == '-' or char == ',' or char == '<':
      result.append('_')
    elif char == '>' or char == ' ':
      continue
    else:
      result.append(char)

  return ''.join(result)


@to_c_name.register(list)
def _(s: list[str]) -> str:
  return to_c_name('_'.join(s))
