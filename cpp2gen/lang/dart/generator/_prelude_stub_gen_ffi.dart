import 'dart:ffi' as ffi;

// dart format off

final class ffi_exception extends ffi.Struct {
  external ffi.Pointer<ffi.Char> message;

  external ffi.Pointer<ffi.Char> location;
}

typedef ffi_exception_t = ffi.Pointer<ffi_exception>;


@ffi.Native<ffi_exception_t Function()>()
external ffi_exception_t maybe_get_last_ffi_exception();

@ffi.Native<ffi.Void Function(ffi_exception_t)>()
external void ffi_exception_destroy(
  ffi_exception_t ex,
);
