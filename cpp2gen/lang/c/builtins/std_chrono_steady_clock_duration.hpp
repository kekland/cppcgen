#include <chrono>

#include "_template.hpp"

struct std_chrono_steady_clock_duration_ref : public ffi_cv<std_chrono_steady_clock_duration_ref, ref<std::chrono::steady_clock::duration>> {};
struct std_chrono_steady_clock_duration : public ffi_cv<std_chrono_steady_clock_duration, std::chrono::steady_clock::duration> {};
typedef std_chrono_steady_clock_duration_ref* std_chrono_steady_clock_duration_ref_t;
typedef std_chrono_steady_clock_duration* std_chrono_steady_clock_duration_t;

// -- hdr

FFI std_chrono_steady_clock_duration_ref_t std_chrono_steady_clock_duration_ref_create(uint64_t milliseconds);
FFI uint64_t std_chrono_steady_clock_duration_count_milliseconds(std_chrono_steady_clock_duration_t instance);

// -- src

FFI std_chrono_steady_clock_duration_ref_t std_chrono_steady_clock_duration_ref_create(uint64_t milliseconds) {
  FFI_FUNCTION_GUARD_BEGIN
  auto duration = std::chrono::steady_clock::duration(std::chrono::milliseconds(milliseconds));
  return std_chrono_steady_clock_duration_ref::wrap(new ref<std::chrono::steady_clock::duration>(duration));
  FFI_FUNCTION_GUARD_END(nullptr)
}

FFI uint64_t std_chrono_steady_clock_duration_count_milliseconds(std_chrono_steady_clock_duration_t instance) {
  FFI_FUNCTION_GUARD_BEGIN
  auto instance_ = std_chrono_steady_clock_duration::unwrap(instance);
  return std::chrono::duration_cast<std::chrono::milliseconds>(*instance_).count();
  FFI_FUNCTION_GUARD_END(0)
}
