# Remove filetype from filename
def name(db):
    return db[:db.find('.')]