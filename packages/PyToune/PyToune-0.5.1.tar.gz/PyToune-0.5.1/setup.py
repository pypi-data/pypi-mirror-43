import os
from setuptools import setup, find_packages

current_file_path = os.path.abspath(os.path.dirname(__file__))

readme_file_path = os.path.join(current_file_path, 'README.md')
with open(readme_file_path, 'r') as f:
    readme = f.read()


packages = find_packages()
setup(
    name='PyToune',
    version='0.5.1',
    author='Frédérik Paradis',
    author_email='fredy_14@live.fr',
    url='https://poutyne.org',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=packages,
    install_requires=['poutyne'],
    python_requires='>=3',
    description='A Keras-like framework and utilities for PyTorch.',
    long_description=readme,
    long_description_content_type='text/markdown',
)
