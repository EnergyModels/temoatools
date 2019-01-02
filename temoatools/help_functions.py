# Remove filetype from filename


def remove_ext(filename):
    """

    :string filename: object
    """
    ind = filename.find('.')
    if not ind == -1:
        return filename[ind]
    else:
        return filename