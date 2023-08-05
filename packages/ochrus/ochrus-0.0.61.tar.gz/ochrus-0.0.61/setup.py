from distutils.core import setup
from io import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'ochrus',
  packages = ['ochrus'], # this must be the same as the name above
  license = 'MIT',
  version = '0.0.61',
  description = 'Ochrus functional test automation infrastructure',
  long_description = long_description,
  author = 'Roni Eliezer',
  author_email = 'roniezr@gmail.com',
  url = 'https://github.com/ochrus/ochrus', # use the URL to the github repo
  download_url = 'https://github.com/ochrus/ochrus-0.0.61.tar.gz',
  keywords = ['functional', 'testing', 'automation', 'infrastructure'], 
  classifiers = [],
  install_requires=['paramiko', 'requests'],
)
