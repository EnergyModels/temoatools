import os
from pathlib import Path

# -----------------------------------------------------
# Remove filetype from filename
# -----------------------------------------------------
def remove_ext(filename):
    """

    :string filename: object
    """
    ind = filename.find('.')
    if not ind == -1:
        return filename[:ind]
    else:
        return filename


# -----------------------------------------------------
# Directory to hold results
# -----------------------------------------------------
def create_results_dir(wrkdir=Path('.'), run_name=''):
    # General results directory
    resultdir = os.path.join(wrkdir, "results")
    try:
        os.stat(resultdir)
    except:
        os.mkdir(resultdir)

    # Results directory specifically for casename
    if len(run_name) > 0:
        resultdir = os.path.join(resultdir, run_name)
        try:
            os.stat(resultdir)
        except:
            os.mkdir(resultdir)

    # Move to directory
    os.chdir(resultdir)
