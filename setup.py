from setuptools import setup

setup(
  name='ValleyBackups',
  version='0.1',
  packages=['valleybackups'],
  py_modules=[
    'valleybackups.db',
    'valleybackups.server'
  ],
  # include_package_data=True,
  install_requires=[
    'Click',
    'pony',
    'boto3==1.2.6',
    'flask'
  ],
  setup_requires=[
    'Click',
    'pony',
    'boto3==1.2.6',
    'flask'
  ],
  entry_points='''
    [console_scripts]
    valleybackups=valleybackups.cli:cli
  '''
)
