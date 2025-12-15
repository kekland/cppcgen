from __future__ import annotations

import pathlib

from ....model import Type
from ....builtins import BuiltinStructure, BuiltinTemplate, BuiltinTemplates
from ....builtins import StdStringTemplate, StdVectorTemplate, StdPairTemplate, StdChronoSteadyClockDurationTemplate, StdOptionalTemplate, StdArrayTemplate, StdFunctionTemplate
from ..utils import to_dart_top_level_name


class DartBuiltinTemplate(BuiltinTemplate):
  def generate_code(self) -> list[str]:
    if not self.template_file_stem: return []

    file_name = pathlib.Path(__file__).parent / f'{self.template_file_stem}.dart'
    with open(file_name, 'r') as f: content = f.read().splitlines()
    content = self.modify_template_file(content)
    content = self.replace_base_name(content)

    code = []
    code_start_index = content.index('// -- code') + 1
    code_end_index = len(content)

    code = content[code_start_index:code_end_index]
    return code


class DartStdStringTemplate(StdStringTemplate, DartBuiltinTemplate): pass
class DartStdVectorTemplate(StdVectorTemplate, DartBuiltinTemplate): pass
class DartStdPairTemplate(StdPairTemplate, DartBuiltinTemplate): pass
class DartStdChronoSteadyClockDurationTemplate(StdChronoSteadyClockDurationTemplate, DartBuiltinTemplate): pass
class DartStdOptionalTemplate(StdOptionalTemplate, DartBuiltinTemplate): pass
class DartStdFunctionTemplate(StdFunctionTemplate, DartBuiltinTemplate): pass


class DartStdArrayTemplate(StdArrayTemplate, DartBuiltinTemplate):
  def modify_template_file(self, lines: list[str]) -> list[str]:
    gen_typedef = []
    gen_to_dart = []
    gen_from_dart = []

    for i in range(self.size):
      gen_typedef.append('ARG1_DART')
      gen_to_dart.append(f'      _getIndex({i})')
      gen_from_dart.append(f'    gen_ffi.std_array_ARG1_SIZE_set(instancePtr, {i}, ARG1_CAST_TO_FFI(value.${i + 1}));')

    gen_typedef = ', '.join(gen_typedef)
    gen_typedef = f'({gen_typedef})'
    gen_to_dart = ',\n'.join(gen_to_dart)
    gen_from_dart = '\n'.join(gen_from_dart)

    # replace all '_std_array_ARG1_DART_SIZE' with gen_typedef
    lines = [l.replace('_array_typedef', gen_typedef) for l in lines]

    # find 'gen:toDart'
    gen_to_dart_index = lines.index('    // gen:toDart') + 1
    lines[gen_to_dart_index] = f'    return (\n{gen_to_dart}\n    );'
    lines.pop(gen_to_dart_index - 1)

    # find 'gen:fromDart'
    gen_from_dart_index = lines.index('    // gen:fromDart') + 1
    lines[gen_from_dart_index] = gen_from_dart
    lines.pop(gen_from_dart_index - 1)

    lines = super().modify_template_file(lines)
    return lines


_templates = BuiltinTemplates(
  std_string=lambda s: DartStdStringTemplate(s),
  std_vector=lambda s: DartStdVectorTemplate(s),
  std_pair=lambda s: DartStdPairTemplate(s),
  std_chrono_steady_clock_duration=lambda s: DartStdChronoSteadyClockDurationTemplate(s),
  std_optional=lambda s: DartStdOptionalTemplate(s),
  std_array=lambda s: DartStdArrayTemplate(s),
  std_function=lambda s: DartStdFunctionTemplate(s),
)


def get_builtin_template(structure: BuiltinStructure) -> DartBuiltinTemplate: return _templates.match(structure)  # type: ignore


def maybe_convert_type_to_builtin(type: Type, resolve_typedef=True) -> Type | None:
  from ..converter.type_converter import convert_type_to_dart
  from ..generator.type_generator import generate_type

  decl_repr = type.decl_repr

  # Convert built-in structures
  if isinstance(decl_repr, BuiltinStructure):
    from ....builtins import StdString, StdVector, StdPair, StdChronoSteadyClockDuration, StdOptional, StdArray, StdSharedPtr, StdUniquePtr, StdFunction

    result: Type | None = None

    if isinstance(decl_repr, StdString):
      result = Type(base_name='String')
    if isinstance(decl_repr, StdVector):
      arg_type = convert_type_to_dart(decl_repr.arg)
      result = Type(base_name=f'List', template_args=[arg_type])
    if isinstance(decl_repr, StdPair):
      first_type = convert_type_to_dart(decl_repr.arg1)
      second_type = convert_type_to_dart(decl_repr.arg2)
      result = Type(base_name=f'({generate_type(first_type)}, {generate_type(second_type)})')
    if isinstance(decl_repr, StdChronoSteadyClockDuration):
      result = Type(base_name='core.Duration')
    if isinstance(decl_repr, StdOptional):
      arg_type = convert_type_to_dart(decl_repr.arg)
      result = Type(base_name=f'{generate_type(arg_type)}?')
    if isinstance(decl_repr, StdArray):
      arg_type = convert_type_to_dart(decl_repr.arg)
      size = decl_repr.size
      arg_str = generate_type(arg_type)
      result = Type(base_name=f'({", ".join([arg_str for _ in range(size)])})')
    if isinstance(decl_repr, StdSharedPtr) or isinstance(decl_repr, StdUniquePtr):
      result = convert_type_to_dart(decl_repr.arg)
    if isinstance(decl_repr, StdFunction):
      result = Type('dynamic') # TODO

    if not result: return None
    if resolve_typedef and decl_repr.typedef:
      return Type(base_name=to_dart_top_level_name(decl_repr.typedef.base.base_name))

    return result
