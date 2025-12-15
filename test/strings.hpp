#include <string>

namespace strings {
class MyClass {
 public:
  MyClass() = default;
  MyClass(const MyClass&) = default;

  std::string concat(const std::string& str1, const std::string& str2);
  std::string repeat(const std::string& str, int times);
  std::string to_upper(const std::string& str);
};
}  // namespace strings