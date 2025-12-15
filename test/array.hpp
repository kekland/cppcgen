#include <array>

namespace test {
class MyClass {
 public:
  MyClass() = default;
  MyClass(const MyClass&) = default;

  std::array<int, 5> create_array();
  int sum_array(const std::array<int, 5>& arr);
};
}  // namespace test