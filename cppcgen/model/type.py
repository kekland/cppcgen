from clang import cindex
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING, Union

from .. import utils

from .parameter import Parameter

if TYPE_CHECKING:
  from .enum import Enum
  from .structure import Structure
  from . import c


@dataclass
# Represents a C/C++ type.
#
# C++ types can be converted to a ffi-compatible C type by calling `.as_c`.
#
# Note: it's deliberately impossible to represent const pointer types (e.g. "int* const") with this structure,
# as I don't think any such types are relevant for the use cases of this project.
class Type:
  base_name: str  # e.g. "vector", "int"
  cindex_type: Optional[cindex.Type] = field(repr=False, default=None)
  namespace: str = ''  # e.g. "std"
  suffix: str = ''  # e.g. _t for C types
  cppdecl_: Optional[Union[Enum, Structure]] = field(default=None, repr=False)
  cdecl_: Optional[Union[c.Enum, c.Structure]] = field(default=None, repr=False)
  template_args: list['Type'] = field(default_factory=list)
  is_pointer: bool = False  # e.g. "int*"
  is_lvalue_reference: bool = False  # e.g. "int&"
  is_rvalue_reference: bool = False  # e.g. "int&&"
  is_const: bool = False  # e.g. "const int"
  is_volatile: bool = False  # e.g. "volatile int"

  @property
  def cindex_decl_cursors(self) -> list[cindex.Cursor]:
    decls = []
    decl = self.cindex_type.get_declaration() if self.cindex_type else None
    if not decl: return decls

    decls.append(decl)
    while decl.kind in [cindex.CursorKind.TYPEDEF_DECL, cindex.CursorKind.TYPE_ALIAS_DECL]:
      _d = decl.underlying_typedef_type.get_declaration()
      if _d.get_usr() == decl.get_usr(): break
      if _d is not None:
        decls.append(_d)
        decl = _d
      else: break

    return decls

  @property
  def cindex_decl_cursor(self) -> Optional[cindex.Cursor]:
    decls = self.cindex_decl_cursors
    if not decls: return None
    return decls[-1]

  @property
  def cindex_decl_usr(self) -> Optional[str]: return self.cindex_decl_cursor.get_usr() if self.cindex_decl_cursor else None

  @property
  def has_template_args(self) -> bool: return len(self.template_args) > 0

  @property
  def is_reference(self) -> bool: return self.is_lvalue_reference or self.is_rvalue_reference

  @property
  def is_pointer_or_reference(self) -> bool: return self.is_pointer or self.is_reference

  @property
  def is_qualified(self) -> bool: return self.is_const or self.is_volatile

  @property
  # Remove const/volatile qualifiers
  def unqualified(self) -> 'Type':
    new_type = self.cindex_type
    if self.is_qualified: new_type = new_type.get_canonical() if new_type else None

    return Type(
      cindex_type=new_type,
      base_name=self.base_name,
      namespace=self.namespace,
      template_args=self.template_args,
      is_pointer=self.is_pointer,
      is_lvalue_reference=self.is_lvalue_reference,
      is_rvalue_reference=self.is_rvalue_reference,
    )

  @property
  # Remove pointer/reference
  def pointee(self) -> 'Type':
    if not self.is_pointer_or_reference: raise ValueError('Type.pointee called on non-pointer/reference type')
    pointee_type = self.cindex_type.get_pointee() if self.cindex_type else None

    return Type(
      cindex_type=pointee_type,
      base_name=self.base_name,
      namespace=self.namespace,
      template_args=self.template_args,
      is_const=self.is_const,
      is_volatile=self.is_volatile,
    )

  @property
  # Remove everything, get the base type
  def base(self) -> 'Type':
    new_type = self
    if new_type.is_pointer_or_reference: new_type = new_type.pointee
    assert new_type is not None
    if new_type.is_qualified: new_type = new_type.unqualified
    return new_type

  @property
  # Return the singular template argument if there is exactly one
  def unwrapped(self) -> 'Type':
    if len(self.template_args) == 1: return self.template_args[0]
    raise ValueError('Type.unwrapped called on type with != 1 template arguments')

  @property
  def decl_typedefs(self) -> 'list[Type]':
    decl_cursors = self.cindex_decl_cursors
    from ..parser import parse_type

    result = [parse_type(cursor.type) for cursor in decl_cursors]
    return result

  def _apply_qualifiers(self, _s: str) -> str:
    s = _s
    if self.is_const: s = f'const {s}'
    if self.is_volatile: s = f'volatile {s}'
    if self.is_lvalue_reference: s = f'{s}&'
    if self.is_rvalue_reference: s = f'{s}&&'
    if self.is_pointer: s = f'{s}*'
    return s

  def _name(self) -> str:
    return self.base_name + self.suffix

  def _name_templated(self) -> str:
    if self.template_args:
      template_args_str = ', '.join([arg.full_name for arg in self.template_args])
      return f'{self._name()}<{template_args_str}>'
    else: return self._name()

  @property
  # namespaced name of the type without qualifiers/generics, e.g. "std::vector"
  def namespaced_base_name(self) -> str: return utils.join_namespace(self.namespace, self._name())

  @property
  # name without namespace but with qualifiers/generics, e.g. "const vector<int>&"
  def name(self) -> str: return self._apply_qualifiers(self._name_templated())

  @property
  # full name of the type, e.g. "const std::vector<int>&"
  def full_name(self) -> str: return self._apply_qualifiers(utils.join_namespace(self.namespace, self._name_templated()))

  @property
  def is_void(self) -> bool: return self.base_name == 'void' and not self.is_pointer_or_reference

  @property
  def is_primitive(self) -> bool: return self.namespace == '' and self.base_name in _primitive_names

  def as_param(self, name: str, default_value: Optional[str] = None) -> 'Parameter':
    return Parameter(
      name=name,
      type=self,
      default_value=default_value,
    )

  # Static set of primitive type names
  @staticmethod
  def void() -> 'Type': return Type(base_name='void')

  @staticmethod
  def boolean() -> 'Type': return Type(base_name='bool')

  @staticmethod
  def char() -> 'Type': return Type(base_name='char')

  @staticmethod
  def char_ptr() -> 'Type': return Type(base_name='char', is_pointer=True)

  @staticmethod
  def const_char_ptr() -> 'Type': return Type(base_name='char', is_pointer=True, is_const=True)

  @property
  def is_decl_enum(self) -> bool:
    from .enum import Enum
    from . import c
    if isinstance(self.cppdecl_, Enum): return True
    if isinstance(self.cdecl_, c.Enum): return True
    return self.cindex_decl_cursor.kind == cindex.CursorKind.ENUM_DECL if self.cindex_decl_cursor else False

  @property
  def is_builtin_structure(self) -> bool:
    from ..converter import builtins
    return builtins.maybe_get_builtin_structure(self) is not None

  @property
  def is_decl_structure(self) -> bool:
    from .structure import Structure
    from . import c
    if isinstance(self.cppdecl_, Structure): return True
    if isinstance(self.cdecl_, c.Structure): return True
    if self.is_builtin_structure: return True
    return self.cindex_decl_cursor.kind in (cindex.CursorKind.STRUCT_DECL, cindex.CursorKind.CLASS_DECL) if self.cindex_decl_cursor else False

  @property
  def as_enum(self) -> Enum:
    from .enum import Enum
    from . import c
    if isinstance(self.cppdecl_, Enum): return self.cppdecl_
    if isinstance(self.cdecl_, c.Enum): return self.cdecl_.base

    from .. import context
    if context.has_enum_by_usr(self.cindex_decl_usr): return context.get_enum_by_usr(self.cindex_decl_usr)  # type: ignore
    from .. import parser
    return parser.parse_enum(self.cindex_decl_cursor)  # type: ignore

  @property
  def as_structure(self) -> Structure:
    from .structure import Structure
    from . import c
    if isinstance(self.cppdecl_, Structure): return self.cppdecl_
    if isinstance(self.cdecl_, c.Structure): return self.cdecl_.base
    if self.is_builtin_structure:
      from ..converter import builtins
      return builtins.get_builtin_structure(self).base

    from .. import context
    if context.has_structure_by_usr(self.cindex_decl_usr): return context.get_structure_by_usr(self.cindex_decl_usr)  # type: ignore
    from .. import parser
    return parser.parse_structure(self.cindex_decl_cursor, type_alias_cursor=self.cindex_type.get_declaration())  # type: ignore

  @property
  def is_c_type(self) -> bool:
    if self.cdecl_ is not None: return True
    if self.is_primitive: return True
    return False

  @property
  def as_c_ptr(self) -> 'Type':
    from ..converter import cpp_type_to_c_ptr
    return cpp_type_to_c_ptr(self)

  @property
  def as_c_ref(self) -> 'Type':
    from ..converter import cpp_type_to_c_ref
    return cpp_type_to_c_ref(self)

  @property
  def ffi_error_default_return(self) -> str:
    if self.is_pointer or self.is_reference: return 'nullptr'
    if self.is_void: return ''
    if self.is_primitive: return '0'
    if self.is_decl_structure: return 'nullptr'
    if self.is_decl_enum: return f'({self.as_enum.as_c.name})0'
    return '0'
    raise ValueError(f'Cannot determine FFI error default return for type {self.full_name}')

  def cast_to_c_ptr(self, var_name: str) -> str:
    from ..generator import generate_type_cast_to_c_ptr
    return generate_type_cast_to_c_ptr(self, var_name)

  def cast_to_c_ref(self, var_name: str) -> str:
    from ..generator import generate_type_cast_to_c_ref
    return generate_type_cast_to_c_ref(self, var_name)

  def cast_to_cpp(self, var_name: str) -> str:
    from ..generator import generate_type_cast_to_cpp
    return generate_type_cast_to_cpp(self, var_name)


_primitive_names = {
  'void',
  'bool',
  'char',
  'short',
  'int',
  'long',
  'long long',
  'unsigned char',
  'unsigned short',
  'unsigned int',
  'unsigned long',
  'unsigned long long',
  'float',
  'double',
  'long double',
}
