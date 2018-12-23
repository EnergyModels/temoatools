# Remove filetype from filename
def remove_ext(filename):
    """

    :string filename: object
    """
    return filename[:filename.find('.')]