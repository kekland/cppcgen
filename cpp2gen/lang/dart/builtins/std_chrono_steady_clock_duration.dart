// ignore_for_file: unused_element, unused_import

import 'dart:core';
import 'dart:core' as core show Duration;
import 'package:ffi/ffi.dart';

import '_template.dart';
import '_gen_ffi.dart' as gen_ffi;

// -- code

extension std_chrono_steady_clock_duration_ext on gen_ffi.std_chrono_steady_clock_duration_t {
  core.Duration toDart() {
    final count = gen_ffi.std_chrono_steady_clock_duration_count_milliseconds(this);
    return core.Duration(milliseconds: count);
  }
}

extension std_chrono_steady_clock_duration_ref_ext on gen_ffi.std_chrono_steady_clock_duration_ref_t {
  gen_ffi.std_chrono_steady_clock_duration_t unwrap() => gen_ffi.std_chrono_steady_clock_duration_ref_unwrap(this);
  void destroy() => gen_ffi.std_chrono_steady_clock_duration_ref_destroy(this);

  static gen_ffi.std_chrono_steady_clock_duration_ref_t fromDart(core.Duration duration, {Arena? arena}) {
    final milliseconds = duration.inMilliseconds;
    final ref = gen_ffi.std_chrono_steady_clock_duration_ref_create(milliseconds);
    arena?.using(ref, (p) => p.destroy());
    return ref;
  }

  core.Duration toDart() {
    final duration = unwrap().toDart();
    destroy();
    return duration;
  }
}

extension _DurationFfiExt on core.Duration {
  gen_ffi.std_chrono_steady_clock_duration_ref_t toFfi({Arena? arena}) => std_chrono_steady_clock_duration_ref_ext.fromDart(this, arena: arena);
  gen_ffi.std_chrono_steady_clock_duration_t toFfiPtr({Arena? arena}) => toFfi(arena: arena).unwrap();
}
