#include <functional>

namespace functions {
class Test {
 public:
  std::function<int(int)> create_function();
  void use_function(const std::function<int(int)>& func, int value);
};
}  // namespace functions