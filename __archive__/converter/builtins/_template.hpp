#include "../../generator/_/templates.hpp"
#include "../../generator/hdr_prelude.hpp"
#include "../../generator/src_prelude.hpp"

#define FFI

using ARG1 = int;
using ARG1_CPP = int;
using ARG1_C_PTR = int*;
using ARG1_C_REF = int*;
#define ARG1_CPP_RET = int
#define ARG1_CPP_PARAMS = int, int
#define ARG1_FFI_ERROR_RETURN 0

ARG1_C_REF CAST1_TO_C_REF(ARG1_CPP value) { return reinterpret_cast<ARG1_C_REF>(&value); }
ARG1_C_PTR CAST1_TO_C_PTR(ARG1_CPP value) { return reinterpret_cast<ARG1_C_PTR>(&value); }
ARG1_CPP& CAST1_TO_CPP(ARG1_C_PTR value) { return *reinterpret_cast<ARG1_CPP*>(&value); }

using ARG2 = int;
using ARG2_CPP = int;
using ARG2_C_PTR = int*;
using ARG2_C_REF = int*;
#define ARG2_CPP_RET = int
#define ARG2_CPP_PARAMS = int, int
#define ARG2_FFI_ERROR_RETURN 0

ARG2_C_REF CAST2_TO_C_REF(ARG2_CPP value) { return reinterpret_cast<ARG2_C_REF>(&value); }
ARG2_C_PTR CAST2_TO_C_PTR(ARG2_CPP value) { return reinterpret_cast<ARG2_C_PTR>(&value); }
ARG2_CPP& CAST2_TO_CPP(ARG2_C_PTR value) { return *reinterpret_cast<ARG2_CPP*>(&value); }
