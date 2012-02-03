from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
setup(
cmdclass = {'build_ext': build_ext},
ext_modules = [Extension("urlist", ["urlist.pyx"])]
)
setup(
cmdclass = {'build_ext': build_ext},
ext_modules = [Extension("urlist_debug", ["urlist_debug.pyx"])]
)
#collector---------------------------------------------------
setup(
cmdclass = {'build_ext': build_ext},
ext_modules = [Extension("communicator", ["communicator.pyx"])]
)
