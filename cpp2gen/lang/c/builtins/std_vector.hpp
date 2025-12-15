#include <vector>

#include "_template.hpp"

struct std_vector_ARG1_ref : public ffi_cv<std_vector_ARG1_ref, ref<std::vector<ARG1_CPP>>> {};
struct std_vector_ARG1 : public ffi_cv<std_vector_ARG1, std::vector<ARG1_CPP>> {};
typedef std_vector_ARG1_ref* std_vector_ARG1_ref_t;
typedef std_vector_ARG1* std_vector_ARG1_t;

// -- hdr

FFI std_vector_ARG1_ref_t std_vector_ARG1_ref_create(size_t size);
FFI size_t std_vector_ARG1_size(std_vector_ARG1_t instance);
FFI ARG1_C_REF std_vector_ARG1_get(std_vector_ARG1_t instance, size_t index);
FFI void std_vector_ARG1_set(std_vector_ARG1_t instance, size_t index, ARG1_C_PTR value);

// -- src

FFI std_vector_ARG1_ref_t std_vector_ARG1_ref_create(size_t size) {
  FFI_FUNCTION_GUARD_BEGIN
  auto vec = std::vector<ARG1_CPP>(size);
  return std_vector_ARG1_ref::wrap(new ref<std::vector<ARG1_CPP>>(vec));
  FFI_FUNCTION_GUARD_END(nullptr)
}

FFI size_t std_vector_ARG1_size(std_vector_ARG1_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_vector_ARG1::unwrap(instance);
  return instance_->size();
  FFI_FUNCTION_GUARD_END(0)
}

FFI ARG1_C_REF std_vector_ARG1_get(std_vector_ARG1_t instance, size_t index) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_vector_ARG1::unwrap(instance);
  return CAST1_TO_C_REF(instance_->at(index));
  FFI_FUNCTION_GUARD_END(ARG1_FFI_ERROR_RETURN)
}

FFI void std_vector_ARG1_set(std_vector_ARG1_t instance, size_t index, ARG1_C_PTR value) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_vector_ARG1::unwrap(instance);
  instance_->at(index) = CAST1_TO_CPP(value);
  FFI_FUNCTION_GUARD_END()
}
