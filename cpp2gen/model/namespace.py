from __future__ import annotations

from dataclasses import dataclass

from .container import Container


@dataclass
# A semantic representation of a namespace.
class Namespace(Container): 
  def __repr_keys__(self): return [*super().__repr_keys__(), 'children']

