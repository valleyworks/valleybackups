from setuptools import setup, find_packages

from valleybackups.__init__ import version

setup(
    name='valleybackups',
    version=version,
    description='Command-line based AWS Glacier backup tool',
    long_description_markdown_filename='README.md',
    url='http://www.valleyworks.us',
    author='Valley Works',
    author_email='valleybackups@valleyworks.us',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='backup glacier aws',
    py_modules=[
        'valleybackups.db',
        'valleybackups.server',
        'valleybackups.extensions.glacier'
    ],
    include_package_data=True,
    install_requires=[
        'Click',
        'pony',
        'boto3==1.2.6',
        'Flask'
    ],
    setup_requires=[
        'Click',
        'pony',
        'boto3==1.2.6',
        'Flask'
    ],
    entry_points='''
    [console_scripts]
    valleybackups=valleybackups.cli:cli
    '''
)
