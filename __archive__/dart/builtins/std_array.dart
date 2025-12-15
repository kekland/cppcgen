import 'package:ffi/ffi.dart';

import '_template.dart';
import '_gen_ffi.dart' as gen_ffi;

// dart format off
// - code

typedef std_array_ARG1_DART_SIZE = (ARG1_DART, ARG1_DART);
std_array_ARG1_DART_SIZE _std_array_ARG1_SIZE_toDart(gen_ffi.std_array_ARG1_SIZE_t ptr) => throw UnimplementedError();
void _std_array_ARG1_SIZE_fromDart(gen_ffi.std_array_ARG1_SIZE_t ptr, std_array_ARG1_DART_SIZE dart) => throw UnimplementedError();

extension std_array_ARG1_SIZE_ext on gen_ffi.std_array_ARG1_SIZE_t {
  std_array_ARG1_DART_SIZE toDart() => _std_array_ARG1_SIZE_toDart(this);
}
