#pragma once

#include <functional>
#include <optional>

namespace mbgl {
class LatLng {};

struct LatLngAltitude {
  LatLng location;
  int altitude = 0;
};

/** Various options for accessing physical properties of the underlying camera
   entity. A direct access to these properties allows more flexible and precise
   controlling of the camera while also being fully compatible and
   interchangeable with CameraOptions. All fields are optional. */
struct FreeCameraOptions {
  /** Helper function for setting the mercator position as Lat&Lng and altitude in meters */
  void setLocation(const LatLngAltitude& location) noexcept;
};

}  // namespace mbgl
