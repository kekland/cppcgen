// ignore_for_file: unused_element, unused_import, library_private_types_in_public_api

import 'package:ffi/ffi.dart';
import '_template.dart';
import '_gen_ffi.dart' as gen_ffi;

typedef _array_typedef = (ARG1_DART,);

// -- code

extension std_array_ARG1_SIZE_ext on gen_ffi.std_array_ARG1_SIZE_t {
  ARG1_DART _getIndex(int i) {
    final v = gen_ffi.std_array_ARG1_SIZE_get(this, i);
    return ARG1_CAST_FROM_FFI(v);
  }

  _array_typedef toDart() {
    // gen:toDart
    return (_getIndex(0),);
  }
}

extension std_array_ARG1_SIZE_ref_ext on gen_ffi.std_array_ARG1_SIZE_ref_t {
  gen_ffi.std_array_ARG1_SIZE_t unwrap() => gen_ffi.std_array_ARG1_SIZE_ref_unwrap(this);
  void destroy() => gen_ffi.std_array_ARG1_SIZE_ref_destroy(this);

  static gen_ffi.std_array_ARG1_SIZE_ref_t fromDart(_array_typedef value, {Arena? arena}) {
    final ref = gen_ffi.std_array_ARG1_SIZE_ref_create();
    final instancePtr = ref.unwrap();

    // gen:fromDart
    gen_ffi.std_array_ARG1_SIZE_set(instancePtr, 0, ARG1_CAST_TO_FFI(value.$1));

    arena?.using(ref, (p) => p.destroy());
    return ref;
  }

  _array_typedef toDart() {
    final result = unwrap().toDart();
    destroy();
    return result;
  }
}

extension _Array_ARG1_SIZE_FfiExt on _array_typedef {
  gen_ffi.std_array_ARG1_SIZE_ref_t toFfi({Arena? arena}) => std_array_ARG1_SIZE_ref_ext.fromDart(this, arena: arena);
  gen_ffi.std_array_ARG1_SIZE_t toFfiPtr({Arena? arena}) => toFfi(arena: arena).unwrap();
}
