from __future__ import annotations


from dataclasses import dataclass, field
from typing import Any, Optional

from .model import Container

_global_context: Optional[Context] = None


@dataclass
class Context(Container):
  name: str = field(init=False, default='')
  parent: Optional[Container] = field(init=False, default=None)

  def __repr_keys__(self): return [*super().__repr_keys__(), 'children']

  @staticmethod
  def set_global(ctx: Context) -> None:
    global _global_context
    _global_context = ctx

  @staticmethod
  def clear_global() -> None:
    global _global_context
    _global_context = None

  @staticmethod
  def g() -> Context:
    global _global_context
    if _global_context is None: raise RuntimeError('Global context is not initialized')
    return _global_context
