#include <string>

namespace aaaa {
class A {
 public:
  double value();
  void withValue(double v);

  const std::string& uriSchemeAlias() const;
  A& withUriSchemeAlias(std::string alias);
};
}  // namespace aaaa