from functools import singledispatch
from typing import Union


# Convert a string to a Dart-compatible top-level name (UpperCamelCase)
def to_dart_top_level_name(s: Union[str, list[str]]) -> str:
  member_name = to_dart_member_name(s)
  if not member_name: return member_name
  return member_name[0].upper() + member_name[1:]


@singledispatch
# Convert a string to a Dart-compatible member name (lowerCamelCase)
def to_dart_member_name(s: Union[str, list[str]]) -> str: raise NotImplementedError()


@to_dart_member_name.register(str)
def _(s: str) -> str:
  result = []

  s = s.replace('ID', 'Id')
  s = s.replace('URL', 'Url')
  s = s.replace('HTTP', 'Http')
  s = s.replace('HTTPS', 'Https')
  s = s.replace('JSON', 'Json')

  capitalize_next = False
  for i, c in enumerate(s):
    if c.isalnum():
      if capitalize_next:
        result.append(c.upper())
        capitalize_next = False
      else:
        result.append(c.lower() if i == 0 else c)
    else:
      capitalize_next = True

  result = ''.join(result)
  result = result[0].lower() + result[1:] if result else result

  if result == 'default': result = 'default_'

  return result


@to_dart_member_name.register(list)
def _(s: list[str]) -> str:
  return to_dart_member_name('_'.join(s))
