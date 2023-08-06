from setuptools import setup, find_packages

setup(
    name = "petrone",
    version = "0.1.58",
    description = "Library for BYROBOT PETRONE",
    author = "BYROBOT",
    author_email = "dev@byrobot.co.kr",
    url = "http://www.byrobot.co.kr",
    packages = find_packages(exclude=['tests']),
    install_requires = [
        'pyserial>=3.4',
        'numpy>=1.15.4',
        'colorama>=0.4.0'],
    long_description = open('README.md').read(),
)
