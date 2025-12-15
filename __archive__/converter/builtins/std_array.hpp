#include <vector>

#include "_template.hpp"

#define SIZE 10

struct std_array_ARG1_SIZE_ref : public ffi_cv<std_array_ARG1_SIZE_ref, ref<std::array<ARG1_CPP, SIZE>>> {};
struct std_array_ARG1_SIZE : public ffi_cv<std_array_ARG1_SIZE, std::vector<ARG1_CPP>> {};
typedef std_array_ARG1_SIZE_ref* std_array_ARG1_SIZE_ref_t;
typedef std_array_ARG1_SIZE* std_array_ARG1_SIZE_t;

// -- hdr

FFI std_array_ARG1_SIZE_ref_t std_array_ARG1_SIZE_ref_create();
FFI size_t std_array_ARG1_SIZE_size(std_array_ARG1_SIZE_t instance);
FFI ARG1_C_REF std_array_ARG1_SIZE_get(std_array_ARG1_SIZE_t instance, size_t index);
FFI void std_array_ARG1_SIZE_set(std_array_ARG1_SIZE_t instance, size_t index, ARG1_C_PTR value);

// -- src

FFI std_array_ARG1_SIZE_ref_t std_array_ARG1_SIZE_ref_create() {
  FFI_FUNCTION_GUARD_BEGIN
  if constexpr (std::is_default_constructible_v<ARG1_CPP>) {
    auto arr = std::array<ARG1_CPP, SIZE>();
    return std_array_ARG1_SIZE_ref::wrap(new ref<std::array<ARG1_CPP, SIZE>>(arr));
  }
  else {
    throw std::runtime_error("Cannot create std::array<ARG1_CPP, SIZE>: ARG1_CPP is not default constructible");
  }
  FFI_FUNCTION_GUARD_END(nullptr)
}

FFI size_t std_array_ARG1_SIZE_size(std_array_ARG1_SIZE_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_array_ARG1_SIZE::unwrap(instance);
  return instance_->size();
  FFI_FUNCTION_GUARD_END(0)
}

FFI ARG1_C_REF std_array_ARG1_SIZE_get(std_array_ARG1_SIZE_t instance, size_t index) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_array_ARG1_SIZE::unwrap(instance);
  return CAST1_TO_C_REF(instance_->at(index));
  FFI_FUNCTION_GUARD_END(ARG1_FFI_ERROR_RETURN)
}

FFI void std_array_ARG1_SIZE_set(std_array_ARG1_SIZE_t instance, size_t index, ARG1_C_PTR value) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_array_ARG1_SIZE::unwrap(instance);
  instance_->at(index) = CAST1_TO_CPP(value);
  FFI_FUNCTION_GUARD_END()
}
