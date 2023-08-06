from setuptools import setup
from os import path



this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyabst',
      setup_requires=['wheel'],
      version='0.0.1',
      author='Joshua David Wood',
      author_email='pyaugment@gmail.com',
      description='A library which generates text summaries allowing users to weight significant or insignificant target words.',
      long_description_content_type='text/markdown',
      long_description=long_description,
      url='https://github.com/joshuadavidwood',
      classifiers=['Programming Language :: Python :: 3',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent'],
      packages=['pyabst'])

