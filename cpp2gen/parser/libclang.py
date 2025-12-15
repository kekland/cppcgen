import clang.cindex
import subprocess
import pathlib

from ..utils import get_logger

logger = get_logger('libclang')


# Configures libclang. Currently only set up for macOS with Homebrew LLVM.
def configure_libclang():
  clang.cindex.Config.set_library_file('/opt/homebrew/opt/llvm/lib/libclang.dylib')


# Returns the path to the macOS SDK.
def get_sdk_path() -> str:
  return subprocess.check_output(['xcrun', '--show-sdk-path']).decode().strip()


# Returns a list of system include directories used by clang on this system.
def get_system_include_dirs() -> list[pathlib.Path]:
  output = subprocess.check_output(['clang++', '-std=c++20', '-stdlib=libc++', '-E', '-x', 'c++', '-', '-v'], input=b'', stderr=subprocess.STDOUT).decode()
  include_dirs = []
  capture = False
  for line in output.splitlines():
    if line.strip() == '#include <...> search starts here:':
      capture = True
      continue
    if line.strip() == 'End of search list.':
      break
    if capture:
      dir_path = line.strip()
      include_dirs.append(pathlib.Path(dir_path))

  return include_dirs


# Parses a translation unit at the given file path (with provided include dirs).
def parse_translation_unit(file_path: pathlib.Path, include_dirs: list[pathlib.Path]) -> clang.cindex.TranslationUnit:
  index = clang.cindex.Index.create()
  sdk_path = get_sdk_path()
  tu = index.parse(
    file_path,
    args=[
      *(f'-I{inc}' for inc in include_dirs),
      '-std=c++20',
      '-x',
      'c++',
      '-stdlib=libc++',
      *(f'-isystem{inc}' for inc in get_system_include_dirs()),
      f'-isysroot{sdk_path}',
    ],
    options=clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES,
  )

  # print diagnostics
  for diag in tu.diagnostics: logger.warning(str(diag))
  return tu
