from __future__ import annotations

from dataclasses import dataclass


# A base class for all model elements.
@dataclass
class Element:
  name: str

  def __repr_keys__(self) -> list[str]: return ['*']

  def __repr_attrs__(self) -> dict[str, object]:
    d = self.__dict__

    keys = self.__repr_keys__()
    always_ignore_keys = ['*', 'parent']
    attrs = {}

    def assign(k, v): 
      if k not in always_ignore_keys: attrs[k] = v

    if keys == ['*']:
      for k, v in d.items(): assign(k, v)
    else:
      for k in keys: 
        try: 
          assign(k, getattr(self, k))
        except AttributeError: pass

    return attrs
