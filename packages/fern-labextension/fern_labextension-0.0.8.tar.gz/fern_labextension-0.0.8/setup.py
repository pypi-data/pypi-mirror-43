import os

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def version():
    "get version from VERSION file"
    version_file = open(os.path.join(ROOT_DIR, 'fern/VERSION'))
    return version_file.read().strip()


setup(
    name='fern_labextension',
    version=version(),
    author='amie',
    author_email='hej@amie.ai',
    license="private",
    description='Fern Jupyter lab Extension',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/disraptoer/fern-next',
    python_requires='>=3.5',
    install_requires=[
        'ipython', 'pandas', 'numpy', 'jupyterlab', 'amieci>=0.0.7'
    ])
