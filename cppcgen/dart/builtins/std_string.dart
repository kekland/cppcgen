import 'package:ffi/ffi.dart';

import '_gen_ffi.dart' as gen_ffi;

// - code

extension std_string_ext on gen_ffi.std_string_t {
  String toDart() {
    final ptr = gen_ffi.std_string_c_str(this);
    final str = ptr.cast<Utf8>().toDartString();
    return str;
  }
}

extension std_string_ref_ext on gen_ffi.std_string_ref_t {
  gen_ffi.std_string_t unwrap() => gen_ffi.std_string_ref_unwrap(this);
  void destroy() => gen_ffi.std_string_ref_destroy(this);

  static gen_ffi.std_string_ref_t fromDart(String str, {Arena? arena}) {
    final cStr = str.toNativeUtf8(allocator: calloc);
    final ref = gen_ffi.std_string_ref_create(cStr.cast());
    calloc.free(cStr);
    arena?.using(ref, (p) => p.destroy());
    return ref;
  }

  String toDart() {
    final str = unwrap().toDart();
    destroy();
    return str;
  }
}

extension StringFfiExt on String {
  gen_ffi.std_string_ref_t toFfi({Arena? arena}) => std_string_ref_ext.fromDart(this, arena: arena);
  gen_ffi.std_string_t toFfiPtr({Arena? arena}) => toFfi(arena: arena).unwrap();
}
