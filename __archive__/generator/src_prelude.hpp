#include <exception>
#include <source_location>
#include <string>
#include <format>

#include "hdr_prelude.hpp"

#define FFI_FUNCTION_GUARD_BEGIN try {
#define FFI_FUNCTION_GUARD_END(RETURN) \
  }                                    \
  catch (const std::exception& e) {    \
    handle_ffi_exception(e);           \
    return RETURN;                     \
  }                                    \
  catch (...) {                        \
    handle_ffi_unknown_exception();    \
    return RETURN;                     \
  }

ffi_exception* _last_exception;

void handle_ffi_exception(const std::exception& e) {
  if (_last_exception) delete _last_exception;

  auto error_msg = e.what();
  auto source = std::source_location::current();
  auto location = std::format("{} at {}:{} ({})", source.file_name(), source.line(), source.column(), source.function_name());

  _last_exception = new ffi_exception{strdup(error_msg), strdup(location.c_str())};
}

void handle_ffi_unknown_exception() {
  if (_last_exception) delete _last_exception;
  _last_exception = new ffi_exception{"Unknown exception"};
}

ffi_exception_t maybe_get_last_ffi_exception() {
  if (_last_exception) {
    ffi_exception* ex = _last_exception;
    _last_exception = nullptr;
    return ex;
  } else {
    return nullptr;
  }
}

void ffi_exception_destroy(ffi_exception_t ex) {
  delete ex;
}
