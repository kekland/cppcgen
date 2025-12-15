from __future__ import annotations

import pathlib
from dataclasses import dataclass, field

from ....utils import code_list_to_str, indent

_hdr_prelude: str
_src_prelude: str

with open(pathlib.Path(__file__).parent / '_prelude.hpp', 'r') as f: _hdr_prelude = f.read()
with open(pathlib.Path(__file__).parent / '_prelude.cpp', 'r') as f: _src_prelude = f.read()

_src_prelude = _src_prelude.replace('\n#include "_prelude.hpp"\n', '')


@dataclass
class GeneratedCode:
  hdr_includes: set[str] = field(default_factory=set)
  src_includes: set[str] = field(default_factory=set)

  hdr_enum_defs: list[list[str]] = field(default_factory=list)
  src_enum_defs: list[list[str]] = field(default_factory=list)
  src_enum_cv_defs: list[list[str]] = field(default_factory=list)

  hdr_struct_defs: list[list[str]] = field(default_factory=list)
  src_struct_defs: list[list[str]] = field(default_factory=list)

  hdr: list[list[str]] = field(default_factory=list)
  src: list[list[str]] = field(default_factory=list)

  def merge(self, other: 'GeneratedCode') -> None:
    self.hdr_includes.update(other.hdr_includes)
    self.src_includes.update(other.src_includes)
    self.hdr_enum_defs.extend(other.hdr_enum_defs)
    self.src_enum_defs.extend(other.src_enum_defs)
    self.src_enum_cv_defs.extend(other.src_enum_cv_defs)
    self.hdr_struct_defs.extend(other.hdr_struct_defs)
    self.src_struct_defs.extend(other.src_struct_defs)
    self.hdr.extend(other.hdr)
    self.src.extend(other.src)

  @property
  def hdr_code(self) -> str:
    c = []

    c.append(_hdr_prelude)

    # Includes
    for include in sorted(self.hdr_includes): c.append(f'#include {include}')
    c.append('')

    # Enum definitions
    for enum_def in self.hdr_enum_defs:
      c.extend(enum_def)
      c.append('')

    # Struct definitions
    for struct_def in self.hdr_struct_defs:
      c.extend(struct_def)
      c.append('')

    # Other header code
    for hdr in self.hdr:
      c.extend(hdr)
      c.append('')

    return code_list_to_str(c)

  @property
  def src_code(self) -> str:
    c = []

    # Includes
    for include in sorted(self.src_includes): c.append(f'#include {include}')
    c.append('')

    c.append(_src_prelude)

    # Enum definitions
    for enum_def in self.src_enum_defs:
      c.extend(enum_def)
      c.append('')

    # Enum cv
    if self.src_enum_cv_defs:
      c.append('// Enum conversion functions')
      c.append('namespace enum_cv {')
      for i in range(len(self.src_enum_cv_defs)):
        c.extend(indent(self.src_enum_cv_defs[i]))
        if i < len(self.src_enum_cv_defs) - 1: c.append('')
      c.append('};')
      c.append('')

    # Struct definitions
    for struct_def in self.src_struct_defs:
      c.extend(struct_def)
      c.append('')

    # Other source code
    for src in self.src:
      c.extend(src)
      c.append('')

    return code_list_to_str(c)

  def finalize(self) -> tuple[str, str]:
    return (self.hdr_code, self.src_code)
