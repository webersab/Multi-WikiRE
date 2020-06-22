#!/usr/bin/env python3

import os
import sys
from pathlib import Path,WindowsPath

if sys.version_info < (3, 5):
    raise RuntimeError('NAMANDA supports Python 3.5 or higher.')

DATA_DIR = (
    os.getenv('NAMANDA_DATA') or
    os.path.join(Path(__file__).absolute().parents[1].as_posix(), 'data')
)

from . import tokenizers
from . import reader
