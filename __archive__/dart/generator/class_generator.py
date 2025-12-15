from ...dart import model as dart
from ... import utils
from .parameter_generator import generate_parameters_cast_block


def generate_class_ffi_extensions(cls: dart.Class) -> list[str]:
  code: list[str] = []
  c_structure = cls.c_structure

  # -- Ref ptr --

  # Destructor method typedef
  if c_structure.destroy_method:
    code.append(f'typedef {c_structure.ref_base_name}_destroy_fn = ffi.NativeFunction<ffi.Void Function(gen_ffi.{c_structure.ref_name})>;')
    code.append(f'ffi.Pointer<{c_structure.ref_base_name}_destroy_fn> get {c_structure.ref_base_name}_destroy_fn_ptr => gen_ffi.addresses.{c_structure.destroy_method.name};')

  code.append(f'extension {c_structure.ref_base_name}_ext on gen_ffi.{c_structure.ref_name} {{')

  # Destructor
  if c_structure.destroy_method:
    code.append(f'  void destroy() => gen_ffi.{c_structure.destroy_method.name}(this);')

  # Unwrap
  if c_structure.unwrap_method: code.append(f'  gen_ffi.{c_structure.name} unwrap() => gen_ffi.{c_structure.unwrap_method.name}(this);')

  # Copy
  code.append(f'  gen_ffi.{c_structure.ref_name} copy() => unwrap().copy();')

  code.append(f'}}')
  code.append('')  

  # -- Value ptr --

  code.append(f'extension {c_structure.base_name}_ext on gen_ffi.{c_structure.name} {{')

  # Copy
  code.append(f'  gen_ffi.{c_structure.ref_name} copy() => gen_ffi.{c_structure.copy_method.name}(this);')

  # Regular methods
  for method in cls.ext_methods:
    code.extend(utils.indent(method.generate_impl()))

  # Field methods
  for name in cls.ext_fields:
    getter, setter = cls.ext_fields[name]
    if getter: code.extend(utils.indent(getter.generate_impl()))
    if setter: code.extend(utils.indent(setter.generate_impl()))

  code.append(f'}}')

  return code


def generate_class(cls: dart.Class) -> list[str]:
  code: list[str] = []

  cpp_structure = cls.cpp_structure
  c_structure = cls.c_structure

  # Helper extensions for FFI interop
  code.extend(generate_class_ffi_extensions(cls))
  code.append('')

  code.append(f'class {cls.name} extends FfiRef<gen_ffi.{c_structure.ref_name}> {{')
  code.append(f'  {cls.name}.fromFfi(super.ptr);')
  code.append(f'')
  code.append(f'  static final _finalizer = ffi.NativeFinalizer({c_structure.ref_base_name}_destroy_fn_ptr.cast());')
  code.append(f'  @override void attachFinalizer() => _finalizer.attach(this, ptr.cast(), detach: this);')
  code.append(f'  @override void detachFinalizer() => _finalizer.detach(this);')
  code.append(f'')

  # Methods
  for method in cls.methods:
    code.extend(utils.indent(method.generate_impl()))

  code.append(f'}}')

  return code
