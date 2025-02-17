from setuptools import setup, Extension
from Cython.Build import cythonize
import os

path: str = os.path.dirname(os.path.abspath(__file__))
custom_name: str = 'cython_fitting_function'

ext_modules: list = [Extension(
    name=custom_name,
    sources=[r".\fitting_function.pyx"],
)]

setup(
    name='fitting_function',
    ext_modules=cythonize(ext_modules),
    options={'build_ext': {'build_lib': path}}
)
