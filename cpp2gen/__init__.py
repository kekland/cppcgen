import pathlib
import subprocess

from .model import Element
from .utils import get_logger, dump_element

logger = get_logger(__name__)


def configure_libclang():
  from .parser.libclang import configure_libclang as configure
  configure()


def parse_and_generate(
  include_dirs: list[pathlib.Path],
  files_to_parse: list[pathlib.Path],
  entities_to_generate: list[str],
  c_output_hdr_file: pathlib.Path,
  c_output_src_file: pathlib.Path,
  dart_output_ffigen_file: pathlib.Path,
  dart_output_bindings_file: pathlib.Path,
):
  from .parser import parse_file
  from .context import Context

  ctx = Context()
  for file_path in files_to_parse:
    logger.info(f'parsing file @ {file_path}')
    file_ctx = parse_file(file_path, include_dirs)
    ctx.merge(file_ctx)

  Context.set_global(ctx)
  logger.info(f'parsing completed, generating code')

  # Collect entities
  entities: list[Element] = []
  if entities_to_generate == ['*']:
    # recursively collect all Structure and Enum elements
    def maybe_collect(e: Element) -> None:
      from .model import Structure, Enum, Container

      if isinstance(e, (Structure, Enum)): entities.append(e)
      if isinstance(e, Container):
        for child in e.children: maybe_collect(child)

    maybe_collect(ctx)
    logger.info(f'automatically collected {len(entities)} entities for code generation')
  else:
    for entity_name in entities_to_generate:
      entity_split = entity_name.split('::')
      entity = ctx.find_child_by_path(entity_split)
      if entity is None: logger.warning(f'entity not found for generation: {entity_name}')
      else: entities.append(entity)

  logger.info(f'starting code generation for {len(entities)} entities')

  # C codegen
  from .lang.c import generator as c_generator
  (c_hdr_code, c_src_code) = c_generator.generate_code(entities, include_dirs, files_to_parse, c_output_hdr_file, c_output_src_file)
  with c_output_hdr_file.open('w', encoding='utf-8') as f: f.write(c_hdr_code)
  with c_output_src_file.open('w', encoding='utf-8') as f: f.write(c_src_code)

  # Dart codegen
  from .lang.dart import generator as dart_generator
  dart_code = dart_generator.generate_code(entities, c_output_hdr_file, dart_output_ffigen_file)
  with dart_output_bindings_file.open('w', encoding='utf-8') as f: f.write(dart_code)

  # Debug dump
  # with pathlib.Path('cpp2gen.parser.out.json').open('w', encoding='utf-8') as f: f.write(dump_element(ctx))

  Context.clear_global()
