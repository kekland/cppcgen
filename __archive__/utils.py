import re
from typing import Union


# Joins a namespace and a name into a fully qualified name.
def join_namespace(namespace: str, name: str) -> str:
  if namespace: return f'{namespace}::{name}'
  else: return name


# Converts a CamelCase string to snake_case.
# e.g. CamelCaseString -> camel_case_string
def camel_case_to_snake_case(camel_case_string):
  # Replace ID with Id
  _str = re.sub(r'ID', 'Id', camel_case_string)
  _str = re.sub(r'URL', 'Url', _str)
  _str = re.sub(r'HTTP', 'Http', _str)
  _str = re.sub(r'HTTPS', 'Https', _str)
  _str = re.sub(r'JSON', 'Json', _str)
  snake_case_string = re.sub(r'(?<!^)(?=[A-Z])', '_', _str).lower()
  return snake_case_string


# Converts a C++ name to a C-style name.
# e.g. MyNamespace::MyClass -> my_namespace_my_class, std::vector -> std_vector
def cpp_name_to_c_name(cpp_name: str) -> str:
  return camel_case_to_snake_case(cpp_name.replace('::', '_').replace('<', '_').replace('>', '_')).replace('__', '_')


# Uncapitalizes the first letter of a string.
def uncapitalize(s: str) -> str:
  if not s:
    return s
  return s[0].lower() + s[1:]


# Capitalizes the first letter of a string.
def capitalize(s: str) -> str:
  if not s:
    return s
  return s[0].upper() + s[1:]


# Indents each line of a given string by the specified number of spaces.
def indent(s: Union[str, list[str]], spaces: int = 2) -> Union[str, list[str]]:
  indent_str = ' ' * spaces
  if isinstance(s, str): return '\n'.join([f'{indent_str}{line}' for line in s.splitlines()])
  elif isinstance(s, list): return [f'{indent_str}{line}' for line in s]
  else: raise TypeError('s must be a string or a list of strings')


# Remove consecutive empty lines
def clean_code(lines: list[str]) -> list[str]:
  cleaned_lines = []
  previous_empty = False
  for line in lines:
    if line.strip() == '':
      if not previous_empty:
        cleaned_lines.append(line)
      previous_empty = True
    else:
      cleaned_lines.append(line)
      previous_empty = False
  return cleaned_lines


# Convert a list[str] of code to a single string with newlines.
def code_list_to_str(code_lines: list[str]) -> str:
  return '\n'.join(clean_code(code_lines))
