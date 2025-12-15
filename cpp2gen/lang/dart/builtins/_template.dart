import 'dart:ffi';

class ARG1_DART {}

ARG1_DART ARG1_CAST_FROM_FFI(Pointer<Void> ptr) => throw UnimplementedError();
ARG1_DART ARG1_CAST_FROM_FFI_COPY(Pointer<Void> ptr) => throw UnimplementedError();
Pointer<Void> ARG1_CAST_TO_FFI(ARG1_DART v) => nullptr;

class ARG2_DART {}

ARG2_DART ARG2_CAST_FROM_FFI(Pointer<Void> ptr) => throw UnimplementedError();
Pointer<Void> ARG2_CAST_TO_FFI(ARG2_DART v) => nullptr;
