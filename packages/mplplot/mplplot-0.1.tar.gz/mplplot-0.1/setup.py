from setuptools import setup

import subprocess

try:  # Try to create an rst long_description from README.md
    args = "pandoc", "--to", "rst", "README.md"
    long_description = subprocess.check_output(args)
    long_description = long_description.decode()
except Exception as error:
    print("README.md conversion to reStructuredText failed. Error:\n",
          error, "Setting long_description to None.")
    long_description = None

setup(
    name='mplplot',
    version='0.1',
    packages=['mplplot'],
    author='Keji Li',
    author_email='mail@keji.li',
    install_requires=['numpy', 'matplotlib', 'seaborn'],
    extras_require={'network': ['networkx']},
    description='matplotlib customizations and customized ploting functions',
    long_description=long_description
)
