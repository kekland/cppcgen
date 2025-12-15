import re

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


def c_name_to_cpp_name(c_name: str) -> str:
  parts = c_name.split('_')
  cpp_name = ''.join(part.capitalize() for part in parts)
  return uncapitalize(cpp_name)


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
