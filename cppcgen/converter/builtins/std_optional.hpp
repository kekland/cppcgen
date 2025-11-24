#include <optional>

#include "_template.hpp"

struct std_optional_ARG1_ref : public ffi_cv<std_optional_ARG1_ref, ref<std::optional<ARG1_CPP>>> {};
struct std_optional_ARG1 : public ffi_cv<std_optional_ARG1, std::optional<ARG1_CPP>> {};
typedef std_optional_ARG1_ref* std_optional_ARG1_ref_t;
typedef std_optional_ARG1* std_optional_ARG1_t;

// -- hdr

FFI std_optional_ARG1_ref_t std_optional_ARG1_ref_create_value(ARG1_C_PTR v);
FFI std_optional_ARG1_ref_t std_optional_ARG1_ref_create_empty();
FFI bool std_optional_ARG1_has_value(std_optional_ARG1_t instance);
FFI ARG1_C_PTR std_optional_ARG1_value(std_optional_ARG1_t instance);
FFI void std_optional_ARG1_reset(std_optional_ARG1_t instance);
FFI void std_optional_ARG1_emplace(std_optional_ARG1_t instance, ARG1_C_PTR value);

// -- src

FFI std_optional_ARG1_ref_t std_optional_ARG1_ref_create_value(ARG1_C_PTR v) {
  FFI_FUNCTION_GUARD_BEGIN
  auto opt = std::optional<ARG1_CPP>(CAST1_TO_CPP(v));
  return std_optional_ARG1_ref::wrap(new ref<std::optional<ARG1_CPP>>(opt));
  FFI_FUNCTION_GUARD_END(nullptr)
}

FFI std_optional_ARG1_ref_t std_optional_ARG1_ref_create_empty() {
  FFI_FUNCTION_GUARD_BEGIN
  auto opt = std::optional<ARG1_CPP>();
  return std_optional_ARG1_ref::wrap(new ref<std::optional<ARG1_CPP>>(opt));
  FFI_FUNCTION_GUARD_END(nullptr)
}

FFI bool std_optional_ARG1_has_value(std_optional_ARG1_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_optional_ARG1::unwrap(instance);
  return instance_->has_value();
  FFI_FUNCTION_GUARD_END(false)
}

FFI ARG1_C_PTR std_optional_ARG1_value(std_optional_ARG1_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_optional_ARG1::unwrap(instance);
  return CAST1_TO_C_PTR(instance_->value());
  FFI_FUNCTION_GUARD_END(ARG1_FFI_ERROR_RETURN)
}

FFI void std_optional_ARG1_reset(std_optional_ARG1_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_optional_ARG1::unwrap(instance);
  instance_->reset();
  FFI_FUNCTION_GUARD_END()
}

FFI void std_optional_ARG1_emplace(std_optional_ARG1_t instance, ARG1_C_PTR value) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_optional_ARG1::unwrap(instance);
  instance_->emplace(CAST1_TO_CPP(value));
  FFI_FUNCTION_GUARD_END()
}
