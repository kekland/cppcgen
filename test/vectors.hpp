#include <string>

namespace vectors {
class MyClass {
 public:
  MyClass() = default;
  MyClass(const MyClass&) = default;

  std::vector<int> create_vector(int n);
  int sum_vector(const std::vector<int>& vec);

  std::vector<std::vector<int>> create_2d_vector(int rows, int cols);

  std::pair<int, float> get_pair();
  std::pair<std::string, std::string> concat_pair(const std::pair<std::string, std::string>& p);
  std::pair<std::vector<std::string>, std::vector<int>> mix_pair(
      const std::pair<std::vector<std::string>, std::vector<int>>& p);
};
}  // namespace vectors