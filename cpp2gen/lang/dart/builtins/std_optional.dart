// ignore_for_file: unused_element, unused_import

import 'package:ffi/ffi.dart';
import '_template.dart';
import '_gen_ffi.dart' as gen_ffi;

// -- code

extension std_optional_ARG1_ext on gen_ffi.std_optional_ARG1_t {
  ARG1_DART? toDart() {
    final hasValue = gen_ffi.std_optional_ARG1_has_value(this);
    if (!hasValue) return null;

    final v = gen_ffi.std_optional_ARG1_value(this);
    return ARG1_CAST_FROM_FFI_COPY(v);
  }
}

extension std_optional_ARG1_ref_ext on gen_ffi.std_optional_ARG1_ref_t {
  gen_ffi.std_optional_ARG1_t unwrap() => gen_ffi.std_optional_ARG1_ref_unwrap(this);
  void destroy() => gen_ffi.std_optional_ARG1_ref_destroy(this);

  static gen_ffi.std_optional_ARG1_ref_t fromDart(ARG1_DART? value, {Arena? arena}) {
    final gen_ffi.std_optional_ARG1_ref_t ref;

    if (value != null) {
      final vFfi = ARG1_CAST_TO_FFI(value);
      ref = gen_ffi.std_optional_ARG1_ref_create_value(vFfi);
    } else {
      ref = gen_ffi.std_optional_ARG1_ref_create_empty();
    }

    arena?.using(ref, (p) => p.destroy());
    return ref;
  }

  ARG1_DART? toDart() {
    final result = unwrap().toDart();
    destroy();
    return result;
  }
}

extension _ARG1_Nullable_FfiExt on ARG1_DART? {
  gen_ffi.std_optional_ARG1_ref_t toFfi({Arena? arena}) => std_optional_ARG1_ref_ext.fromDart(this, arena: arena);
  gen_ffi.std_optional_ARG1_t toFfiPtr({Arena? arena}) => toFfi(arena: arena).unwrap();
}
