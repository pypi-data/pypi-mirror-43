#!/usr/bin/python3 -S
import os
import uuid
from setuptools import setup, Extension
from pkgutil import walk_packages
from Cython.Build import cythonize
from distutils.command.build_ext import build_ext

pathname = os.path.dirname(os.path.realpath(__file__))


PKG = 'kola'
PKG_NAME = 'kola-bottle'
PKG_VERSION = '0.2.2'


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return (line for line in lineiter if line and not line.startswith("#"))

install_reqs = parse_requirements(pathname + "/requirements.txt")


def find_packages(prefix=""):
    path = [prefix]
    yield prefix
    prefix = prefix + "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name


class _build_ext(build_ext):
    def run(self):
        build_ext.run(self)

    def build_extension(self, ext):
        build_ext.build_extension(self, ext)


# Cythonizes MultiDict
extensions = cythonize([
    Extension('kola.multidict', [pathname + '/kola/multidict.pyx'])])


setup(
    name=PKG_NAME,
    version=PKG_VERSION,
    description='A WSGI framework for Python 3 based upon Bottle.',
    author='Jared Lunde',
    author_email='jared.lunde@gmail.com',
    url='https://github.com/jaredlunde/kola',
    license="MIT",
    install_requires=list(install_reqs),
    packages=list(find_packages(PKG)),
    ext_modules=extensions,
    cmdclass=dict(build_ext=_build_ext)
)
