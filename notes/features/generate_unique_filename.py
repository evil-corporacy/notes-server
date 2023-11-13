import os
from generate_random_string import generate_random_string


def generate_unique_filename(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return 'uploads/{0}{1}'.format(generate_random_string(32), file_extension)
