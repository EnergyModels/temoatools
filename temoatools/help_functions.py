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
def create_results_dir(wrkdir=os.path.normcase('.'), run_name=''):
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


# -----------------------------------------------------
# Directory to hold results
# -----------------------------------------------------
def create_dir(project_path=os.path.normcase('.'), optional_dir='results'):
    # configs - required
    dir = os.path.join(project_path, "configs")
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    # databases directory - required
    dir = os.path.join(project_path, "databases")
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    # optional directory
    if len(optional_dir)>0:
        dir = os.path.join(project_path, optional_dir)
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)