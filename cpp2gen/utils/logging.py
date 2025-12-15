import logging
import os


def get_logger(name: str) -> logging.Logger:
  return logging.getLogger(os.path.basename(name))
