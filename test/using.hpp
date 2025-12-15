#include <array>
#include <optional>

namespace test {
using vec3 = std::array<float, 3>;

class Test {
 public:
  Test() = default;
  Test(const Test&) = default;

  vec3 add(const vec3& a, const vec3& b);
  vec3 scale(const vec3& v, float factor);

  std::optional<vec3> maybe_get_vector(bool return_vector);
};

}  // namespace test