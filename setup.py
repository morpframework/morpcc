from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='dlcc',
      version=version,
      description="Data Lake Control Center",
      long_description="""\
A data lake management tool built on top of MorpFW""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='datalake dataengineering bigdata datacatalog',
      author='Izhar Firdaus',
      author_email='kagesenshi.87@gmail.com',
      url='http://github.com/koslab/dlcc',
      license='AGPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "morpfw",
          "more.chameleon",
          "more.static"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
