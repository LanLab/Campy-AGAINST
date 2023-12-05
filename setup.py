import os.path
import sys

from setuptools import setup,find_packages
from campy-against import __version__
import zipfile

def readme():
    with open('README.md') as f:
        return f.read()


def extract_zip(zip_file, destination):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)

zip_file_path = os.path.join(os.path.dirname(__file__), 'campy-against', 'Resources', 'Reference_genomes.zip')
extracted_dir = os.path.join(os.path.dirname(__file__), 'campy-against', 'Resources')

extract_zip(zip_file_path, extracted_dir)

package_data = []
for root, dirs, files in os.walk(extracted_dir):
    for file in files:
        file_path = os.path.relpath(os.path.join(root, file), extracted_dir)
        package_data.append(file_path)


setup(name='campy-against',
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
      url='https://github.com/LanLab/campy-against',
      author='Ruochen Wu',
      author_email='ruochen.wu@unsw.edu.au',
      license='GPLv3',
      packages=['campy-against', 'campy-against.resources'],
      include_package_data=True,
      entry_points={
          'console_scripts': ['campy-against=campy-against.campy-against:main'],
      },
      package_data={"campy-against": package_data
      },
      zip_safe=False)
