#include <chrono>
#include <optional>

namespace test {
using Clock = std::chrono::steady_clock;
using Duration = Clock::duration;

class MyClass {
 public:
  Duration get_duration_in_seconds(int seconds);
  std::optional<Duration> maybe_get_duration();
};
}  // namespace test