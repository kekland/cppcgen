from __future__ import annotations

from dataclasses import dataclass

from .container import Container


@dataclass
# A semantic representation of a namespace.
class Namespace(Container): pass
