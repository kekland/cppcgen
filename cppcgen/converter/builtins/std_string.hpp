#include <string>

#include "_template.hpp"

struct std_string_ref : public ffi_cv<std_string_ref, ref<std::string>> {};
struct std_string : public ffi_cv<std_string, std::string> {};
typedef std_string_ref* std_string_ref_t;
typedef std_string* std_string_t;

// -- hdr

FFI std_string_ref_t std_string_ref_create(const char* c_str);
FFI size_t std_string_length(std_string_t instance);
FFI void std_string_resize(std_string_t instance, size_t new_size);
FFI const char* std_string_c_str(std_string_t instance);
FFI char* std_string_data(std_string_t instance);

// -- src

FFI std_string_ref_t std_string_ref_create(const char* c_str) {
  FFI_FUNCTION_GUARD_BEGIN
  auto str = std::string(c_str);
  return std_string_ref::wrap(new ref<std::string>(str));
  FFI_FUNCTION_GUARD_END(nullptr)
}

FFI size_t std_string_length(std_string_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_string::unwrap(instance);
  return instance_->length();
  FFI_FUNCTION_GUARD_END(0)
}

FFI void std_string_resize(std_string_t instance, size_t new_size) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_string::unwrap(instance);
  instance_->resize(new_size);
  FFI_FUNCTION_GUARD_END()
}

FFI const char* std_string_c_str(std_string_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_string::unwrap(instance);
  return instance_->c_str();
  FFI_FUNCTION_GUARD_END(nullptr)
}

FFI char* std_string_data(std_string_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_string::unwrap(instance);
  return instance_->data();
  FFI_FUNCTION_GUARD_END(nullptr)
}
