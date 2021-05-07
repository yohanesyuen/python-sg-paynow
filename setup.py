import setuptools
from version import *

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="sgpaynow",
    version=VERSION,
    author="Yohanes Yuen",
    author_email="yuen.wei.ping@gmail.com",
    description="Library for generating Singapore Paynow QR code",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.6',
)
