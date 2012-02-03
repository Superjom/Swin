from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

#judger---------------------------------------------------
setup(
cmdclass = {'build_ext': build_ext},
ext_modules = [Extension("judger", ["judger.py"])]
)

#saver---------------------------------------------------
setup(
cmdclass = {'build_ext': build_ext},
ext_modules = [Extension("saver", ["saver.pyx"])]
)
