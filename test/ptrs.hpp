#include <memory>

namespace forward_decl {
class LatLngBounds {
 public:
  std::unique_ptr<LatLngBounds> extend(const LatLngBounds& area) const noexcept;

  std::shared_ptr<LatLngBounds> shared_extend(const LatLngBounds& area) const noexcept;

  LatLngBounds* ptr_extend(const LatLngBounds& area) const noexcept;
};
}  // namespace forward_decl