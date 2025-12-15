// ignore_for_file: unused_element

import 'package:ffi/ffi.dart';

import '_template.dart';
import '_gen_ffi.dart' as gen_ffi;

// -- code

extension std_vector_ARG1_ext on gen_ffi.std_vector_ARG1_t {
  List<ARG1_DART> toDart() {
    final length = gen_ffi.std_vector_ARG1_size(this);
    final list = List<ARG1_DART>.generate(length, (i) {
      final v = gen_ffi.std_vector_ARG1_get(this, i);
      return ARG1_CAST_FROM_FFI(v);
    });

    return list;
  }
}

extension std_vector_ARG1_ref_ext on gen_ffi.std_vector_ARG1_ref_t {
  gen_ffi.std_vector_ARG1_t unwrap() => gen_ffi.std_vector_ARG1_ref_unwrap(this);
  void destroy() => gen_ffi.std_vector_ARG1_ref_destroy(this);

  static gen_ffi.std_vector_ARG1_ref_t fromDart(List<ARG1_DART> list, {Arena? arena}) {
    final ref = gen_ffi.std_vector_ARG1_ref_create(list.length);
    final instancePtr = ref.unwrap();

    for (var i = 0; i < list.length; i++) {
      final elem = list[i];
      gen_ffi.std_vector_ARG1_set(instancePtr, i, ARG1_CAST_TO_FFI(elem));
    }

    arena?.using(ref, (p) => p.destroy());
    return ref;
  }

  List<ARG1_DART> toDart() {
    final result = unwrap().toDart();
    destroy();
    return result;
  }
}

extension _List_ARG1_FfiExt on List<ARG1_DART> {
  gen_ffi.std_vector_ARG1_ref_t toFfi({Arena? arena}) => std_vector_ARG1_ref_ext.fromDart(this, arena: arena);
  gen_ffi.std_vector_ARG1_t toFfiPtr({Arena? arena}) => toFfi(arena: arena).unwrap();
}
