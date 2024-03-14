import os.path
import sys

from setuptools import setup,find_packages
from campygstyper import __version__
import zipfile

def readme():
    with open('README.md') as f:
        return f.read()

genomedir = os.path.join(os.path.dirname(__file__), 'campygstyper', 'Resources')


package_data = []
for root, dirs, files in os.walk(genomedir):
    for file in files:
        file_path = os.path.relpath(os.path.join(root, file), genomedir)
        package_data.append(file_path)


setup(name='campygstyper',
      version=__version__,
      description='assignment of ANI genomic species to Campylobacter genomes',
      long_description=readme(),
      classifiers=[
          'License :: OSI Approved :: GPLv3',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Medical Science Apps.',
          'Intended Audience :: Science/Research',
      ],
      keywords='genomic taxonomy campylobacter',
      url='https://github.com/LanLab/campyagainst',
      author='Ruochen Wu',
      author_email='ruochen.wu@unsw.edu.au',
      license='GPLv3',
      packages=['campygstyper', 'campygstyper.resources'],
      include_package_data=True,
      entry_points={
          'console_scripts': ['campygstyper=campygstyper.campygstyper:main'],
      },
      package_data={"campygstyper": package_data
      },
      zip_safe=False)
