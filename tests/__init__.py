import os

TEMP_DIR='tmp/tests'
def setup_package():
    import pdb; pdb.set_trace()
    os.remove('{}/*'.format(TEMP_DIR))
