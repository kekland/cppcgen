#include <memory>
#include <optional>

namespace optional {
class MyClass {
 public:
  MyClass() = default;
  MyClass(const MyClass&) = default;

  std::optional<int> create_optional(int value, bool has_value);
  int get_optional_value(const std::optional<int>& opt, int default_value);
};
}