# Installing Packages Locally from Source
# python setup.py install --user
# For installing using: pip install .
# Go into this directory firstly

# python setup.py sdist bdist_wheel
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# twine upload dist/*

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='myimpy',
      version='1.5',
      description='Imaging processing methods',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/JinhangZhu/myimpy',
      author='Jinhang Zhu',
      author_email='jinhang.d.zhu@gmail.com',
      license='MIT',
      packages=['myimpy'],
      package_dir={'jinhang': 'myimpy'},
      package_data={'jinhang':['*.*', 'myimpy/*']},
      zip_safe=False)