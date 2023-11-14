import os
from generate_id import generate_id


def generate_unique_filename(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return 'uploads/{0}{1}'.format(generate_id(), file_extension)
