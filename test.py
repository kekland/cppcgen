import cppcgen
import pathlib
import logging
import sys
from rich.logging import RichHandler

root_dir = pathlib.Path(__file__).parent


class DimDebugRichHandler(RichHandler):
  def render_message(self, record, message):
    renderable = super().render_message(record, message)

    # wrap debug messages in gray style
    if record.levelno == logging.DEBUG:
      from rich.style import Style
      from rich.text import Text
      if isinstance(renderable, Text):
        renderable.style = Style(dim=True)
    return renderable


logging.basicConfig(
  level=logging.DEBUG,
  format='%(message)s',
  datefmt='',
  handlers=[DimDebugRichHandler(rich_tracebacks=True, show_time=False)]
)

logger = logging.getLogger('cppcgen')

case_ = sys.argv[1] if len(sys.argv) > 1 else '*'

for test_file in (root_dir / 'test').glob('*.hpp'):
  test_name = test_file.stem
  if case_ != '*' and case_ != test_name:
    logger.debug(f'Skipping test case: {test_name}')
    continue

  logger.info(f'Parsing file: {test_file}')
  cppcgen.parse_and_generate(
    files_to_parse=[test_file],
    entities_to_generate_=['*'],
    include_dirs=[root_dir / 'test' / 'include', root_dir / 'test'],
    output_src_file=root_dir / 'test' / f'{test_file.stem}.gen.cpp',
    output_hdr_file=root_dir / 'test' / f'{test_file.stem}.gen.h',
  )
