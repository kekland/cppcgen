from __future__ import annotations

from ....model import Structure
from ....utils import get_logger, indent
from ....builtins import maybe_get_builtin_structure

logger = get_logger(__name__)


def generate_structure(struct: Structure, force_builtin=False) -> list[str]:
  if not force_builtin and maybe_get_builtin_structure(struct.type) is not None: return []

  from ...c import converter as c_converter
  from .. import converter as dart_converter
  from .type_generator import generate_type
  from .method_generator import generate_method_impl

  logger.debug(f'generating Dart code for structure: {struct.full_name_cpp_str}')
  dart_struct = dart_converter.convert_structure(struct)
  c_struct = c_converter.convert_structure(struct)

  code = []
  ptr_type_str = generate_type(c_struct.type_ptr)
  ref_ptr_type_str = generate_type(c_struct.ref.type_ptr)

  # Destructor function pointer
  def _destructor_function_pointer():
    code.append(f'// Destructor function pointer for {c_struct.ref.name}')
    code.append(f'typedef {c_struct.ref.name}_destroy_fn = ffi.NativeFunction<ffi.Void Function({ref_ptr_type_str})>;')
    code.append(f'ffi.Pointer<{c_struct.ref.name}_destroy_fn> get {c_struct.ref.name}_destroy_fn_ptr => gen_ffi.addresses.{c_struct.ref_destroy_method.name};')

  _destructor_function_pointer()
  code.append(f'')

  # Extension methods for ref ptr
  def _ref_extension_methods():
    code.append(f'// Helper extension methods for {c_struct.ref.name} (ref<{struct.full_name_cpp_str}>)')
    code.append(f'extension {c_struct.ref.name}_ext on {ref_ptr_type_str} {{')

    # Destructor/unwrap/copy
    code.append(f'  @_inline void destroy() => _ffiCall(() => gen_ffi.{c_struct.ref_destroy_method.name}(this));')
    code.append(f'  @_inline {ptr_type_str} unwrap() => _ffiCall(() => gen_ffi.{c_struct.ref_unwrap_method.name}(this));')
    code.append(f'  @_inline {ref_ptr_type_str} copy() => unwrap().copy();')

    # Methods
    if len(dart_struct.ref_ext_methods) > 0: code.append(f'')
    for m in dart_struct.ref_ext_methods: code.extend(indent(generate_method_impl(m)))

    code.append(f'}}')

  _ref_extension_methods()
  code.append(f'')

  def _extension_methods():
    code.append(f'// Helper extension methods for {c_struct.name} ({struct.full_name_cpp_str})')
    code.append(f'extension {c_struct.name}_ext on {ptr_type_str} {{')

    # Copy
    code.append(f'  @_inline {ref_ptr_type_str} copy() => _ffiCall(() => gen_ffi.{c_struct.copy_method.name}(this));')

    # Methods
    if len(dart_struct.ext_methods) > 0: code.append(f'')
    for m in dart_struct.ext_methods: code.extend(indent(generate_method_impl(m)))

    code.append(f'}}')

  _extension_methods()
  code.append(f'')

  def _class_decl():
    code.append(f'// Representation of {struct.full_name_cpp_str}')
    code.append(f'final class {dart_struct.name} extends FfiRef<{ref_ptr_type_str}> {{')
    code.append(f'  {dart_struct.name}.fromFfi(super.ptr);')

    # Constructors
    if len(dart_struct.regular_constructors) > 0: code.append(f'')
    for ctor in dart_struct.regular_constructors:
      code.extend(indent(generate_method_impl(ctor)))
      code.append(f'')

    code.append(f'  static final _finalizer = ffi.NativeFinalizer({c_struct.ref.name}_destroy_fn_ptr.cast());')
    code.append(f'  @override void _attachFinalizer() => _finalizer.attach(this, ptr.cast(), detach: this);')
    code.append(f'  @override void _detachFinalizer() => _finalizer.detach(this);')

    # Methods
    code.append(f'')
    for m in dart_struct.methods:
      code.extend(indent(generate_method_impl(m)))
      code.append(f'')

    if not dart_struct.field_methods: code.pop()

    # Fields
    last_field_name = None
    for m in dart_struct.field_methods:
      if last_field_name and last_field_name != m.name: code.append(f'')

      code.extend(indent(generate_method_impl(m)))
      last_field_name = m.name

    code.append(f'}}')

  _class_decl()
  return code
