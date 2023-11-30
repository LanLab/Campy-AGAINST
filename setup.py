import os.path
import sys

from setuptools import setup,find_packages
from dodge import __version__
from setuptools.command.install import install
import zipfile

def readme():
    with open('README.md') as f:
        return f.read()


class CustomInstallCommand(install):
    def run(self):
        # Call the default install command
        install.run(self)

        # Extract your zip file after installation
        zip_file_path = 'CampyAGAINST/resources/Reference_genomes.zip'
        extraction_path = 'CampyAGAINST/resources/'
        if os.path.exists(zip_file_path):
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extraction_path)
        else:
            sys.exit(f"{zip_file_path} does not exist")
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
      url='https://github.com/LanLab/Campy-AGAINST',
      author='Ruochen Wu',
      author_email='ruochen.wu@unsw.edu.au',
      license='GPLv3',
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          'console_scripts': ['campyagainst=CampyAGAINST.CampyAGAINST:main'],
      },
      cmdclass={
        'install': CustomInstallCommand,
      },
      zip_safe=False)
