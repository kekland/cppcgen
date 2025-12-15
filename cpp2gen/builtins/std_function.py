from __future__ import annotations

from dataclasses import dataclass, field

from ._model import BuiltinStructure, BuiltinTemplate
from ..model import Container, Namespace, Type, Parameter
from ._utils import modify_template_file_arg
from ..lang.c.utils import to_c_name


@dataclass
class StdFunction(BuiltinStructure):
  name: str = field(default='function', init=False)
  parent: Container | None = field(default_factory=lambda: Namespace('std'), init=False)

  def setup(self) -> None: 
    self.name = f'function<{self.return_type.full_name_cpp_str}({", ".join(param.type.full_name_cpp_str for param in self.parameters)})>'
    self.c_name = f'std_function_{self.fn_type_name}'

  @property
  def _func_type(self) -> Type: return self.type_.template_args[0]  # type: ignore

  @property
  def return_type(self) -> Type: return self._func_type.function_return_type  # type: ignore

  @property
  def parameters(self) -> list[Parameter]: return self._func_type.function_parameters  # type: ignore

  @property
  def fn_type_name(self) -> str:
    return f'{to_c_name(self.return_type.full_name_cpp_str.lower())}$' + '_'.join(map(lambda x: to_c_name(x.type.full_name_cpp_str).lower(), self.parameters))


@dataclass
class StdFunctionTemplate(BuiltinTemplate):
  @property
  def _func_type(self) -> Type: return self.type_.template_args[0]  # type: ignore

  @property
  def return_type(self) -> Type: return self._func_type.function_return_type  # type: ignore

  @property
  def parameters(self) -> list[Parameter]: return self._func_type.function_parameters  # type: ignore

  @property
  def template_file_stem(self) -> str: return 'std_function'

  @property
  def fn_type_name(self) -> str:
    return f'{to_c_name(self.return_type.full_name_cpp_str.lower())}$' + '_'.join(map(lambda x: to_c_name(x.type.full_name_cpp_str).lower(), self.parameters))

  @property
  def base_name_impl(self) -> str: return f'std_function_{self.fn_type_name}'

  def modify_template_file(self, lines: list[str]) -> list[str]:
    lines = modify_template_file_arg(lines, self._func_type, 1)
    return lines
