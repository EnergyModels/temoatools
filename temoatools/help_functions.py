import os

#-----------------------------------------------------
# Remove filetype from filename
#-----------------------------------------------------
def remove_ext(filename):
    """

    :string filename: object
    """
    ind = filename.find('.')
    if not ind == -1:
        return filename[ind]
    else:
        return filename


#-----------------------------------------------------
# Directory to hold results
#-----------------------------------------------------
def create_results_dir(wrkdir='.', run_name=''):
    # General results directory
    resultdir = wrkdir + "\\results"
    try:
        os.stat(resultdir)
    except:
        os.mkdir(resultdir)

    # Results directory specifically for casename
    if len(run_name) > 0:
        resultdir = wrkdir + "\\results" + "\\" + run_name
        try:
            os.stat(resultdir)
        except:
            os.mkdir(resultdir)

    # Move to directory
    os.chdir(resultdir)