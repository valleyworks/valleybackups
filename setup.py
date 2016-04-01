from setuptools import setup, find_packages

setup(
    name='valleybackups',
    version='0.1.2',
    description='Command-Line based backup software '
                'for peace of mind',
    long_description_markdown_filename='README.md',
    url='https://github.com/valleyworks/valleybackups',
    author='ValleyWorks',
    author_email='nahuel.chaves@valleyworks.us',
    #packages=['valleybackups'],
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
