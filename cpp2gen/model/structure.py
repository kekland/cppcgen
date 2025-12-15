from __future__ import annotations

from dataclasses import dataclass

from .container import Container
from .constructor import Constructor
from .method import Method
from .field import Field
from .synthetic_field import SyntheticField
from .type import Type


@dataclass
# A semantic representation of a structure (class/struct/etc).
class Structure(Container):
  #
  # -- Constructors
  #

  @property
  def constructors(self) -> list[Constructor]: return [c for c in self.children if type(c) is Constructor]

  @property
  def regular_constructors(self) -> list[Constructor]: return [c for c in self.constructors if not c.is_move and not c.is_copy]

  @property
  def factory_methods(self) -> list[Method]: return [m for m in self.static_methods if m.return_type == self.type]

  #
  # -- Methods
  #

  @property
  def methods(self) -> list[Method]: return [m for m in self.children if type(m) is Method]

  @property
  def static_methods(self) -> list[Method]: return [m for m in self.methods if m.is_static]

  @property
  def static_nonfactory_methods(self) -> list[Method]: return [m for m in self.static_methods if m.return_type != self.type]

  @property
  def instance_methods(self) -> list[Method]: return [m for m in self.methods if not m.is_static and not m.is_operator]

  @property
  def operator_methods(self) -> list[Method]: return [m for m in self.methods if m.is_operator]

  #
  # -- Fields
  #

  @property
  def all_fields(self) -> list[Field]: return [f for f in self.children if isinstance(f, Field)]

  @property
  def real_fields(self) -> list[Field]: return [f for f in self.all_fields if type(f) is Field]

  @property
  def synthetic_fields(self) -> list[SyntheticField]: return [f for f in self.all_fields if isinstance(f, SyntheticField)]

  def __repr_keys__(self): return [*super().__repr_keys__(), 'constructors', 'factory_methods', 'methods', 'all_fields']
