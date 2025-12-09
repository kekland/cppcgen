import 'dart:ffi';

import 'package:ffi/ffi.dart';

class ARG1_DART {}

ARG1_DART ARG1_CAST_FROM_FFI(Pointer<Void> ptr) => throw UnimplementedError();
Pointer<Void> ARG1_CAST_TO_FFI(ARG1_DART v, {Arena? arena}) => nullptr;
