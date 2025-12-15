from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
  from .parameter import Parameter
  from .container import Container


@dataclass
# A semantic representation of a type.
class Type:
  base_name: str  # e.g. 'int', 'vector', 'MyClass'
  namespace: list[str] = field(default_factory=list)  # e.g. '[std]'
  template_args: list['Type | str'] = field(default_factory=list)  # either Type or raw literals (e.g. std::array<int, 5>)
  typedefs: list[Type] = field(default_factory=list)
  decl_repr_: Optional[Container] = None
  function_return_type: Optional['Type'] = None  # for function types
  function_parameters: list[Parameter] = field(default_factory=list)  # for function types

  is_function: bool = False  # e.g. std::function<int(int)>
  is_pointer: bool = False  # e.g. int*
  is_lvalue_reference: bool = False  # e.g. int&
  is_rvalue_reference: bool = False  # e.g. int&&
  is_const: bool = False  # e.g. const int
  is_volatile: bool = False  # e.g. volatile int

  @property
  def base(self) -> 'Type':
    return Type(
      base_name=self.base_name,
      namespace=self.namespace,
      template_args=self.template_args,
      decl_repr_=self.decl_repr_,
    )

  @property
  def decl_repr(self) -> Optional[Container]:
    if self.decl_repr_ is not None: return self.decl_repr_

    from ..builtins import maybe_get_builtin_structure
    if builtin := maybe_get_builtin_structure(self): return builtin

    from .container import Container
    from ..context import Context

    elem = Context.g().find_child_by_path([*self.namespace, self.base_name])
    if isinstance(elem, Container): return elem
    return None

  @property
  def full_name_cpp_str(self) -> str:
    parts = [*self.namespace, self.base_name]
    base = '::'.join(parts)
    if self.template_args:
      args = ', '.join([arg.full_name_cpp_str if isinstance(arg, Type) else str(arg) for arg in self.template_args])
      base += f'<{args}>'

    if self.is_pointer: base += '*'
    if self.is_lvalue_reference: base += '&'
    if self.is_rvalue_reference: base += '&&'
    if self.is_const: base = 'const ' + base
    if self.is_volatile: base = 'volatile ' + base

    return base

  def as_param(self, name: str) -> Parameter:
    from .parameter import Parameter
    return Parameter(type=self, name=name)

  def _is_lang(self, lang_attr: str) -> bool:
    if not self.decl_repr: return False
    return getattr(self.decl_repr, lang_attr, False)

  @property
  def is_cpp(self) -> bool: return self._is_lang('is_cpp')

  @property
  def is_c(self) -> bool: return self._is_lang('is_c')

  @property
  def is_dart(self) -> bool: return self._is_lang('is_dart')

  def __eq__(self, other):
    if not isinstance(other, Type): return False
    return self.full_name_cpp_str == other.full_name_cpp_str

  def toJSON(self) -> str: return self.full_name_cpp_str

  # List of commonly used types

  @staticmethod
  def void() -> Type: return Type(base_name='void')
