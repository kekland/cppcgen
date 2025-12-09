from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
# A semantic representation of a type.
class Type:
  base_name: str  # e.g. 'int', 'vector', 'MyClass'
  namespace: list[str] = field(default_factory=list)  # e.g. '[std]'
  template_args: list['Type | str'] = field(default_factory=list)  # either Type or raw literals (e.g. std::array<int, 5>)

  is_pointer: bool = False  # e.g. int*
  is_lvalue_reference: bool = False  # e.g. int&
  is_rvalue_reference: bool = False  # e.g. int&&
  is_const: bool = False  # e.g. const int
  is_volatile: bool = False  # e.g. volatile int

  def __eq__(self, other):
    if not isinstance(other, Type): return False
    return self.__dict__ == other.__dict__
