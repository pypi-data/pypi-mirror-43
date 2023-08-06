from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fern_labextension',
    version='0.0.7',
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
