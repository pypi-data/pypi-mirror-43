# Installing Packages Locally from Source
# python setup.py install --user
# For installing using: pip install .
# Go into this directory firstly

from setuptools import setup

setup(name='myimpy',
      version='1.1',
      description='Imaging processing methods',
      url='https://github.com/JinhangZhu/myimpy',
      author='Jinhang Zhu',
      author_email='jinhang.d.zhu@gmail.com',
      license='MIT',
      packages=['myimpy'],
      package_dir={'jinhang': 'myimpy'},
      package_data={'jinhang':['*.*', 'myimpy/*']},
      zip_safe=False)