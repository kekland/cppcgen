#include <exception>
#include <source_location>
#include <string>
#include <format>

#include "_prelude.hpp"

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

// A reference wrapper to manage ownership semantics across FFI.
template <typename T>
struct ref {
 public:
  ref() : ptr(std::make_shared<T>()) {}
  explicit ref(T* v) : ptr(v, [](T* v) {}) {}
  ref(const T& v) : ptr(std::make_shared<T>(v)) {}
  ref(T&& v) : ptr(std::make_shared<T>(std::move(v))) {}
  explicit ref(std::shared_ptr<T> v) : ptr(std::move(v)) {}
  explicit ref(std::unique_ptr<T> v) : ptr(std::move(v)) {}

  T& get() { return *ptr; }
  T* unwrap() { return ptr.get(); }

  std::shared_ptr<T> as_shared() { return ptr; }
  std::unique_ptr<T> as_unique() {
    if (ptr.use_count() != 1) return nullptr;
    auto unique = std::make_unique<T>(std::move(*ptr));
    ptr.reset();
    return unique;
  }

 private:
  std::shared_ptr<T> ptr;
};

// A helper structure to easily wrap/unwrap C/C++ types.
template <typename CType, typename CppType>
struct ffi_cv {
  inline static CType* wrap(CppType* ref_ptr) { return reinterpret_cast<CType*>(ref_ptr); }
  inline static CType* wrap(CppType& ref) { return reinterpret_cast<CType*>(&ref); }
  inline static CppType* unwrap(void* raw) { return reinterpret_cast<CppType*>(raw); }
};
