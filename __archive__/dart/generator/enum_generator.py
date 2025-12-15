from ...dart import model as dart


def generate_enum(e: dart.Enum) -> list[str]:
  code: list[str] = []
  c_enum = e.c_enum

  # Enum declaration
  code.append(f'enum {e.name} {{')

  i = 0
  for k, v in e.values.items():
    is_last = i == len(e.values) - 1
    d = ',' if not is_last else ';'
    code.append(f'  {k}({v}){d}')
    i += 1

  code.append(f'')

  # Constructor and value field
  code.append(f'  const {e.name}(this.value);')
  code.append(f'  final int value;')
  code.append(f'')

  # Enum from FFI method
  code.append(f'  static {e.name} fromFfi(gen_ffi.{c_enum.name} v) => switch (v) {{')
  for i in range(len(e.values)):
    c_value = c_enum.values[i]
    dart_value = list(e.values.keys())[i]
    code.append(f'    gen_ffi.{c_enum.name}.{c_value.name} => {e.name}.{dart_value},')
  
  code.append(f'  }};')
  code.append(f'')

  # Enum to FFI method
  code.append(f'  gen_ffi.{c_enum.name} toFfi() => switch (this) {{')
  for i in range(len(e.values)):
    c_value = c_enum.values[i]
    dart_value = list(e.values.keys())[i]
    code.append(f'    {e.name}.{dart_value} => gen_ffi.{c_enum.name}.{c_value.name},')
  
  code.append(f'  }};')
  code.append(f'}}')

  return code
