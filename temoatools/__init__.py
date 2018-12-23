

import os

# functions from temoatools
from .help_functions import remove_ext
from .move_data_to_universal_db import move_data_to_db
from .temoa_model_build import build
from .temoa_model_run import run

# storing where resources folder is
resource_path = os.path.join(os.path.split(__file__)[0], "resources")
print resource_path