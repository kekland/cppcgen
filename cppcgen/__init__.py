import pathlib

from logging import getLogger
from typing import Union, Any
from clang import cindex

from . import parser, context, generator
from .converter.builtins import _used_builtins
from .model import cpp


_logger = getLogger('cppcgen')


# Parse given [files_to_parse] with libclang using provided [include_dirs],
# and generate code for specified [entities_to_generate] into output files.
def parse_and_generate(
  include_dirs: list[pathlib.Path],
  files_to_parse: list[pathlib.Path],
  entities_to_generate_: list[str],
  output_hdr_file: pathlib.Path,
  output_src_file: pathlib.Path,
  hdr_prelude: list[str] = [],
  src_prelude: list[str] = [],
):
  entities_to_generate_ = entities_to_generate_
  should_populate_entities = entities_to_generate_ == ['*']

  if should_populate_entities:
    _logger.info('Automatically determining entities to generate...')
    entities_to_generate_ = []

  for file in files_to_parse:
    met_entities = parser.parse_file(file, include_dirs)
    if should_populate_entities: entities_to_generate_.extend(list(map(lambda e: e.full_name, met_entities)))

  if should_populate_entities:
    _logger.info(f'Automatically determined entities to generate ({len(entities_to_generate_)}): {entities_to_generate_}')

  entities: list[Any] = []
  for entity_name in entities_to_generate_:
    e = context.get_entity(entity_name)
    if e is None:
      _logger.warning(f'Entity to generate not found: {entity_name}')
      continue

    entities.append(e)

  code = generator.GeneratedCode(hdr=[hdr_prelude.copy()], src=[src_prelude.copy()])

  # Prepare includes
  code.merge(generator.generate_includes(
    include_dirs=include_dirs,
    files_to_parse=files_to_parse,
    output_hdr_file=output_hdr_file,
    output_src_file=output_src_file,
  ))

  # Templates
  code.merge(generator.generate_templates())

  # Entities
  for entity in entities:
    entity_code = generator.generate(entity)
    code.merge(entity_code)

  # Builtins
  code.merge(generator.generate_builtins())

  hdr_code = code.hdr_code
  src_code = code.src_code

  # Append header include to source file
  include_directive = f'#include "{output_hdr_file.name}"\n\n'
  src_code = include_directive + src_code

  _logger.info(f'Writing generated code to: {output_hdr_file} and {output_src_file}')
  with output_hdr_file.open('w', encoding='utf-8') as hdr_f: hdr_f.write(hdr_code)
  with output_src_file.open('w', encoding='utf-8') as src_f: src_f.write(src_code)
  _logger.info('Code generation completed.')

  context.clear()
  _used_builtins.clear()
