#pragma once

#include <optional>

namespace mbgl {

/**
 * @brief Holds options to limit what parts of a map are visible. All fields are
 * optional.
 */
struct BoundOptions {
    /// Sets the minimum zoom level
    BoundOptions& withMinZoom(double z) {
        minZoom = z;
        return *this;
    }
    /// Sets the maximum zoom level
    BoundOptions& withMaxZoom(double z) {
        maxZoom = z;
        return *this;
    }
    /// Sets the minimum pitch
    BoundOptions& withMinPitch(double p) {
        minPitch = p;
        return *this;
    }
    /// Sets the maximum pitch
    BoundOptions& withMaxPitch(double p) {
        maxPitch = p;
        return *this;
    }

    /// Maximum zoom level allowed.
    std::optional<double> maxZoom;

    /// Minimum zoom level allowed.
    std::optional<double> minZoom;

    /// Maximum pitch allowed in degrees.
    std::optional<double> maxPitch;

    /// Minimum pitch allowed in degrees.
    std::optional<double> minPitch;
};

} // namespace mbgl
