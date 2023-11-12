from setuptools import setup, find_packages

with open('README.md', 'r') as f:
  long_description = f.read()

VERSION = '0.0.1'
DESCRIPTION = 'Threading module extension'

# Setting up
setup(
  name = 'threads',
  version = VERSION,
  author = 'caffeine-addictt (Jun Xiang)',
  author_email = '<junxiangng63@gmail.com>',
  description = DESCRIPTION,
  long_description_content_type = 'text/markdown',
  long_description = long_description,
  packages = find_packages(where = 'src'),
  install_requires = [],
  keywords = ['python', 'threading', 'multiprocessing'],
  classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
  ],
)