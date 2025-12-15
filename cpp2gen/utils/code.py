from __future__ import annotations

from typing import Union


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


# Indents each line of a given string by the specified number of spaces.
def indent(s: Union[str, list[str]], spaces: int = 2) -> Union[str, list[str]]:
  indent_str = ' ' * spaces
  if isinstance(s, str): return '\n'.join([f'{indent_str}{line}' for line in s.splitlines()])
  elif isinstance(s, list): return [f'{indent_str}{line}' for line in s]
  else: raise TypeError('s must be a string or a list of strings')
