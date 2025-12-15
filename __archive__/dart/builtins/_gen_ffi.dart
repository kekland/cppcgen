import 'dart:ffi';

// dart format off

// - std_string

final class std_string_ref extends Opaque {}
final class std_string extends Opaque {}

typedef std_string_ref_t = Pointer<std_string_ref>;
typedef std_string_t = Pointer<std_string>;

std_string_ref_t std_string_ref_create(Pointer<Char> c_str) => nullptr;
std_string_t std_string_ref_unwrap(std_string_ref_t ref) => nullptr;
void std_string_ref_destroy(std_string_ref_t ref) {}
Pointer<Char> std_string_c_str(std_string_t str) => nullptr;

// - std_vector_ARG1

final class std_vector_ARG1_ref extends Opaque {}
final class std_vector_ARG1 extends Opaque {}

typedef std_vector_ARG1_ref_t = Pointer<std_vector_ARG1_ref>;
typedef std_vector_ARG1_t = Pointer<std_vector_ARG1>;

std_vector_ARG1_ref_t std_vector_ARG1_ref_create(int size) => nullptr;
std_vector_ARG1_t std_vector_ARG1_ref_unwrap(std_vector_ARG1_ref_t ref) => nullptr;
void std_vector_ARG1_ref_destroy(std_vector_ARG1_ref_t ref) {}
void std_vector_ARG1_set(std_vector_ARG1_t instance, int index, Pointer<Void> value) {}
int std_vector_ARG1_size(std_vector_ARG1_t instance) => 0;
Pointer<Void> std_vector_ARG1_get(std_vector_ARG1_t instance, int index) => nullptr;

// - std_array_ARG1_SIZE

final class std_array_ARG1_SIZE_ref extends Opaque {}
final class std_array_ARG1_SIZE extends Opaque {}

typedef std_array_ARG1_SIZE_ref_t = Pointer<std_array_ARG1_SIZE_ref>;
typedef std_array_ARG1_SIZE_t = Pointer<std_array_ARG1_SIZE>;

std_array_ARG1_SIZE_ref_t std_array_ARG1_SIZE_ref_create() => nullptr;
Pointer<Void> std_array_ARG1_SIZE_get(std_array_ARG1_SIZE_t instance, Pointer<Void> index) => nullptr;
void std_array_ARG1_SIZE_set(std_array_ARG1_SIZE_t instance, int index, Pointer<Void> value) {}

// dart format on
