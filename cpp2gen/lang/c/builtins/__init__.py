from __future__ import annotations

import pathlib

from ..generator._generator import GeneratedCode
from ....builtins import BuiltinStructure, BuiltinTemplate, BuiltinTemplates
from ....builtins import StdStringTemplate, StdVectorTemplate, StdPairTemplate, StdChronoSteadyClockDurationTemplate, StdOptionalTemplate, StdArrayTemplate, StdFunctionTemplate


class CBuiltinTemplate(BuiltinTemplate):
  def generate_code(self) -> GeneratedCode:
    if not self.template_file_stem: return GeneratedCode()

    file_name = pathlib.Path(__file__).parent / f'{self.template_file_stem}.hpp'
    with open(file_name, 'r') as f: content = f.read().splitlines()
    content = self.modify_template_file(content)
    content = self.replace_base_name(content)

    code = GeneratedCode()
    hdr_start_index = content.index('// -- hdr') + 1
    hdr_end_index = content.index('// -- src')
    src_start_index = hdr_end_index + 1
    src_end_index = len(content)

    code.hdr = [content[hdr_start_index:hdr_end_index]]
    code.src = [content[src_start_index:src_end_index]]

    return code


class CStdStringTemplate(StdStringTemplate, CBuiltinTemplate): pass
class CStdVectorTemplate(StdVectorTemplate, CBuiltinTemplate): pass
class CStdPairTemplate(StdPairTemplate, CBuiltinTemplate): pass
class CStdChronoSteadyClockDurationTemplate(StdChronoSteadyClockDurationTemplate, CBuiltinTemplate): pass
class CStdOptionalTemplate(StdOptionalTemplate, CBuiltinTemplate): pass
class CStdArrayTemplate(StdArrayTemplate, CBuiltinTemplate): pass
class CStdFunctionTemplate(StdFunctionTemplate, CBuiltinTemplate): pass


_templates = BuiltinTemplates(
  std_string=lambda s: CStdStringTemplate(s),
  std_vector=lambda s: CStdVectorTemplate(s),
  std_pair=lambda s: CStdPairTemplate(s),
  std_chrono_steady_clock_duration=lambda s: CStdChronoSteadyClockDurationTemplate(s),
  std_optional=lambda s: CStdOptionalTemplate(s),
  std_array=lambda s: CStdArrayTemplate(s),
  std_function=lambda s: CStdFunctionTemplate(s),
)


def get_builtin_template(structure: BuiltinStructure) -> CBuiltinTemplate: return _templates.match(structure)  # type: ignore
