from setuptools import setup

setup(
  name='ValleyBackups',
  version='0.1',
  py_modules=['valleybackups'],
  install_requires=[
    'Click',
    'pony',
    'boto3'
  ],
  entry_points='''
    [console_scripts]
    valleybackups=valleybackups:cli
  '''
)