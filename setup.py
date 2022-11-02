import os
from setuptools import setup, find_packages

root_dir_path = os.path.dirname(os.path.abspath(__file__))

long_description = open(os.path.join(root_dir_path, 'README.md')).read()

setup(
    name='eyesonly',
    version='0.0.1',
    author='Diego J. Romero López',
    author_email='diegojromerolopez@gmail.com',
    description='A package to avoid having leaks of secrets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=[
        'tomli >= 1.1.0 ; python_version < "3.11"'
    ],
    license='MIT',
    keywords=('secrets', 'leaks', 'isolation'),
    url='https://github.com/diegojromerolopez/eyesonly',
    packages=find_packages(),
    data_files=[],
    include_package_data=True,
    scripts=[]
)
