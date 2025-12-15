// ignore_for_file: unused_element

import 'package:ffi/ffi.dart';

import '_template.dart';
import '_gen_ffi.dart' as gen_ffi;

// -- code

extension std_pair_ARG1_ARG2_ext on gen_ffi.std_pair_ARG1_ARG2_t {
  (ARG1_DART, ARG2_DART) toDart() {
    final v1 = gen_ffi.std_pair_ARG1_ARG2_get_first(this);
    final v2 = gen_ffi.std_pair_ARG1_ARG2_get_second(this);
    return (ARG1_CAST_FROM_FFI(v1), ARG2_CAST_FROM_FFI(v2));
  }
}

extension std_pair_ARG1_ARG2_ref_ext on gen_ffi.std_pair_ARG1_ARG2_ref_t {
  gen_ffi.std_pair_ARG1_ARG2_t unwrap() => gen_ffi.std_pair_ARG1_ARG2_ref_unwrap(this);
  void destroy() => gen_ffi.std_pair_ARG1_ARG2_ref_destroy(this);

  static gen_ffi.std_pair_ARG1_ARG2_ref_t fromDart(ARG1_DART v1, ARG2_DART v2, {Arena? arena}) {
    final p1 = ARG1_CAST_TO_FFI(v1);
    final p2 = ARG2_CAST_TO_FFI(v2);
    final ref = gen_ffi.std_pair_ARG1_ARG2_ref_create(p1, p2);
    arena?.using(ref, (p) => p.destroy());
    return ref;
  }

  (ARG1_DART, ARG2_DART) toDart() {
    final result = unwrap().toDart();
    destroy();
    return result;
  }
}

extension _Pair_ARG1_ARG2_FfiExt on (ARG1_DART, ARG2_DART) {
  gen_ffi.std_pair_ARG1_ARG2_ref_t toFfi({Arena? arena}) => std_pair_ARG1_ARG2_ref_ext.fromDart($1, $2, arena: arena);
  gen_ffi.std_pair_ARG1_ARG2_t toFfiPtr({Arena? arena}) => toFfi(arena: arena).unwrap();
}
