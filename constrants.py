import os
import environ
from os.path import join, dirname, abspath


env_path_file = join(dirname(dirname(abspath(__file__))), '.env')

API_KEY = os.environ.get('API_KEY')