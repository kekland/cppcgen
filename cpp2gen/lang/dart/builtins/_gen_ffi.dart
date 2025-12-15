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

// - std_pair_ARG1_ARG2

final class std_pair_ARG1_ARG2_ref extends Opaque {}
final class std_pair_ARG1_ARG2 extends Opaque {}

typedef std_pair_ARG1_ARG2_ref_t = Pointer<std_pair_ARG1_ARG2_ref>;
typedef std_pair_ARG1_ARG2_t = Pointer<std_pair_ARG1_ARG2>;

std_pair_ARG1_ARG2_ref_t std_pair_ARG1_ARG2_ref_create(Pointer<Void> first, Pointer<Void> second) => nullptr;
std_pair_ARG1_ARG2_t std_pair_ARG1_ARG2_ref_unwrap(std_pair_ARG1_ARG2_ref_t ref) => nullptr;
void std_pair_ARG1_ARG2_ref_destroy(std_pair_ARG1_ARG2_ref_t ref) {}
Pointer<Void> std_pair_ARG1_ARG2_get_first(std_pair_ARG1_ARG2_t instance) => nullptr;
Pointer<Void> std_pair_ARG1_ARG2_get_second(std_pair_ARG1_ARG2_t instance) => nullptr;
void std_pair_ARG1_ARG2_set_first(std_pair_ARG1_ARG2_t instance, Pointer<Void> value) {}
void std_pair_ARG1_ARG2_set_second(std_pair_ARG1_ARG2_t instance, Pointer<Void> value) {}

// - std_chrono_steady_clock_duration

final class std_chrono_steady_clock_duration_ref extends Opaque {}
final class std_chrono_steady_clock_duration extends Opaque {}

typedef std_chrono_steady_clock_duration_ref_t = Pointer<std_chrono_steady_clock_duration_ref>;
typedef std_chrono_steady_clock_duration_t = Pointer<std_chrono_steady_clock_duration>;

std_chrono_steady_clock_duration_ref_t std_chrono_steady_clock_duration_ref_create(int milliseconds) => nullptr;
std_chrono_steady_clock_duration_t std_chrono_steady_clock_duration_ref_unwrap(std_chrono_steady_clock_duration_ref_t ref) => nullptr;
void std_chrono_steady_clock_duration_ref_destroy(std_chrono_steady_clock_duration_ref_t ref) {}
int std_chrono_steady_clock_duration_count_milliseconds(std_chrono_steady_clock_duration_t instance) => 0;

// - std_optional_ARG1

final class std_optional_ARG1_ref extends Opaque {}
final class std_optional_ARG1 extends Opaque {}

typedef std_optional_ARG1_ref_t = Pointer<std_optional_ARG1_ref>;
typedef std_optional_ARG1_t = Pointer<std_optional_ARG1>;

std_optional_ARG1_ref_t std_optional_ARG1_ref_create_value(Pointer<Void> v) => nullptr;
std_optional_ARG1_ref_t std_optional_ARG1_ref_create_empty() => nullptr;
std_optional_ARG1_t std_optional_ARG1_ref_unwrap(std_optional_ARG1_ref_t ref) => nullptr;
void std_optional_ARG1_ref_destroy(std_optional_ARG1_ref_t ref) {}
bool std_optional_ARG1_has_value(std_optional_ARG1_t instance) => false;
Pointer<Void> std_optional_ARG1_value(std_optional_ARG1_t instance) => nullptr;
void std_optional_ARG1_reset(std_optional_ARG1_t instance) {}
void std_optional_ARG1_emplace(std_optional_ARG1_t instance, Pointer<Void> value) {}

// - std_array_ARG1_SIZE

final class std_array_ARG1_SIZE_ref extends Opaque {}
final class std_array_ARG1_SIZE extends Opaque {}

typedef std_array_ARG1_SIZE_ref_t = Pointer<std_array_ARG1_SIZE_ref>;
typedef std_array_ARG1_SIZE_t = Pointer<std_array_ARG1_SIZE>;

std_array_ARG1_SIZE_ref_t std_array_ARG1_SIZE_ref_create() => nullptr;
std_array_ARG1_SIZE_t std_array_ARG1_SIZE_ref_unwrap(std_array_ARG1_SIZE_ref_t ref) => nullptr;
void std_array_ARG1_SIZE_ref_destroy(std_array_ARG1_SIZE_ref_t ref) {}
int std_array_ARG1_SIZE_size(std_array_ARG1_SIZE_t instance) => 0;
Pointer<Void> std_array_ARG1_SIZE_get(std_array_ARG1_SIZE_t instance, int index) => nullptr;
void std_array_ARG1_SIZE_set(std_array_ARG1_SIZE_t instance, int index, Pointer<Void> value) {}