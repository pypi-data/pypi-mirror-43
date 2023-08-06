# coding:utf-8

from distutils.core import setup
from setuptools import find_packages


PACKAGE = "translators"
NAME = "translators"
DESCRIPTION = "Free & Easy translators for Python, such as Google, NetEase(Youdao), etc."
AUTHOR = "UlionTse"
AUTHOR_EMAIL = "shinalone@outlook.com"
URL = "https://github.com/shinalone/translators"
VERSION = __import__(PACKAGE).__version__

with open('README.rst','r',encoding='utf-8') as file:
    long_description = file.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    keywords=['translate','translators','translator','fanyi','Google','Youdao','NetEase'],
    install_requires=[
        'requests>=2.9.1',
        'PyExecJS>=1.2.0'
    ],
    zip_safe=False,
)
