from setuptools import setup, find_packages

with open('README.md', 'r') as f:
  long_description = f.read()

VERSION = '0.0.1'
DESCRIPTION = 'Threading module extension'

# Setting up
setup(
  name = 'thread',
  version = VERSION,
  author = 'caffeine-addictt (Jun Xiang)',
  author_email = '<junxiangng63@gmail.com>',
  description = DESCRIPTION,
  long_description_content_type = 'text/markdown',
  long_description = long_description,

  packages = find_packages(),
  install_requires = ['numpy==1.26.2'],
  keywords = ['python', 'threading', 'multiprocessing'],
  classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3 :: Only',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
  ],
  python_requires = '>=3.11',

  project_urls = {
    'Bug Reports': 'https://github.com/caffeine-addictt/thread/issues',
    'Source': 'https://github.com/caffeine-addictt/thread/'
  }
)