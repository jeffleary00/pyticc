import setuptools
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyticc',
    version='0.0.5',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='Python module to interface with Texas Instruments CCx Sub-1Ghz RF transceivers over SPI.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jeff Leary',
    author_email='sillymonkeysoftware@gmail.com',
    url='https://github.com/jeffleary00/pyticc',
    install_requires=[
        'spidev'
    ],
)
