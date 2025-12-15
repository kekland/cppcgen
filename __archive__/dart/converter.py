from . import model


def convert_type_to_dart(type: model.Type) -> model.Type:
  if type.cpp_type is None: return type

  cpp_type = type.cpp_type
  if cpp_type.is_decl_enum: return model.Type(cpp_type.as_enum.name, cpp_type=cpp_type)

  return type


def convert_parameter_to_dart(param: model.Parameter) -> model.Parameter:
  return model.Parameter(convert_type_to_dart(param.type), param.name)


def convert_method_to_dart(method: model.Method) -> model.Method:
  parameters = [convert_parameter_to_dart(param) for param in method.parameters]
  return model.Method(
    return_type=convert_type_to_dart(method.return_type),
    name=method.name,
    impl=method.impl,
    parameters=parameters,
    is_getter=method.is_getter,
    is_setter=method.is_setter,
    is_static=method.is_static,
    cpp_method=method.cpp_method,
  )


def generate_cast_to_ffi(type: model.Type, var_name: str) -> str:
  if type.cpp_type is None: return var_name

  cast = var_name

  cpp_type = type.cpp_type
  if cpp_type.is_decl_enum: cast = f'{cast}.toFfi()'

  return cast


def generate_cast_from_ffi(type: model.Type, var_name: str) -> str:
  if type.cpp_type is None: return var_name

  cast = var_name

  cpp_type = type.cpp_type
  if cpp_type.is_decl_enum:
    enum = cpp_type.as_enum
    cast = f'{enum.name}.fromFfi({cast})'
  elif cpp_type.is_decl_structure:
    structure = cpp_type.as_structure
    cls = model.Class(structure)
    cast = f'{cls.name}.fromPtr({cast})'

  return cast


def generate_parameters_cast_block(params: list[model.Parameter], parameter_suffix: str = '_') -> list[str]:
  code: list[str] = []

  for param in params:
    code.append(f'final {param.name}{parameter_suffix} = {generate_cast_to_ffi(param.type, param.name)};')

  return code
