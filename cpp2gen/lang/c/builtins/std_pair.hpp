#include <vector>

#include "_template.hpp"

struct std_pair_ARG1_ARG2_ref : public ffi_cv<std_pair_ARG1_ARG2_ref, ref<std::pair<ARG1_CPP, ARG2_CPP>>> {};
struct std_pair_ARG1_ARG2 : public ffi_cv<std_pair_ARG1_ARG2, std::pair<ARG1_CPP, ARG2_CPP>> {};
typedef std_pair_ARG1_ARG2_ref* std_pair_ARG1_ARG2_ref_t;
typedef std_pair_ARG1_ARG2* std_pair_ARG1_ARG2_t;

// -- hdr

FFI std_pair_ARG1_ARG2_ref_t std_pair_ARG1_ARG2_ref_create(ARG1_C_PTR first, ARG2_C_PTR second);
FFI ARG1_C_REF std_pair_ARG1_ARG2_get_first(std_pair_ARG1_ARG2_t instance);
FFI ARG2_C_REF std_pair_ARG1_ARG2_get_second(std_pair_ARG1_ARG2_t instance);
FFI void std_pair_ARG1_ARG2_set_first(std_pair_ARG1_ARG2_t instance, ARG1_C_PTR value);
FFI void std_pair_ARG1_ARG2_set_second(std_pair_ARG1_ARG2_t instance, ARG2_C_PTR value);

// -- src

FFI std_pair_ARG1_ARG2_ref_t std_pair_ARG1_ARG2_ref_create(ARG1_C_PTR first, ARG2_C_PTR second) {
  FFI_FUNCTION_GUARD_BEGIN
  auto pair = std::pair<ARG1_CPP, ARG2_CPP>(CAST1_TO_CPP(first), CAST2_TO_CPP(second));
  return std_pair_ARG1_ARG2_ref::wrap(new ref<std::pair<ARG1_CPP, ARG2_CPP>>(pair));
  FFI_FUNCTION_GUARD_END(nullptr)
}

FFI ARG1_C_REF std_pair_ARG1_ARG2_get_first(std_pair_ARG1_ARG2_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_pair_ARG1_ARG2::unwrap(instance);
  return CAST1_TO_C_REF(instance_->first);
  FFI_FUNCTION_GUARD_END(ARG1_FFI_ERROR_RETURN)
}

FFI ARG2_C_REF std_pair_ARG1_ARG2_get_second(std_pair_ARG1_ARG2_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_pair_ARG1_ARG2::unwrap(instance);
  return CAST2_TO_C_REF(instance_->second);
  FFI_FUNCTION_GUARD_END(ARG2_FFI_ERROR_RETURN)
}

FFI void std_pair_ARG1_ARG2_set_first(std_pair_ARG1_ARG2_t instance, ARG1_C_PTR value) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_pair_ARG1_ARG2::unwrap(instance);
  instance_->first = CAST1_TO_CPP(value);
  FFI_FUNCTION_GUARD_END()
}

FFI void std_pair_ARG1_ARG2_set_second(std_pair_ARG1_ARG2_t instance, ARG2_C_PTR value) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_pair_ARG1_ARG2::unwrap(instance);
  instance_->second = CAST2_TO_CPP(value);
  FFI_FUNCTION_GUARD_END()
}
