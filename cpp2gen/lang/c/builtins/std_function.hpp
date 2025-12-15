#include <vector>

#include "_template.hpp"

struct std_function_ARG1_ref : public ffi_cv<std_function_ARG1_ref, ref<std::function<ARG1_CPP>>> {};
struct std_function_ARG1 : public ffi_cv<std_function_ARG1, std::function<ARG1_CPP>> {};
typedef std_function_ARG1_ref* std_function_ARG1_ref_t;
typedef std_function_ARG1* std_function_ARG1_t;

// -- hdr

FFI BASE_NAME_ref_t BASE_NAME_ref_create(ARG1_CPP_RET (*ptr)(ARG1_CPP_PARAMS));

// -- src

FFI BASE_NAME_ref_t BASE_NAME_ref_create(ARG1_CPP_RET (*ptr)(ARG1_CPP_PARAMS)) {
  FFI_FUNCTION_GUARD_BEGIN
  auto func = std::function<ARG1_CPP>(*ptr);
  return BASE_NAME_ref::wrap(new ref<std::function<ARG1_CPP>>(func));
  FFI_FUNCTION_GUARD_END(nullptr)
}
