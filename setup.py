from setuptools import setup, Extension
import pybind11 

pybind11_include = pybind11.get_include()

ext_modules = [
    Extension(
        'netpbm_cpp',
        ['netpbm.cpp', 'bindings.cpp'],
        include_dirs=[pybind11_include], 
        language='c++',
        extra_compile_args=['/std:c++17', '/O2'],
    ),
]

setup(
    name='netpbm_cpp',
    version='0.0.1',
    description='Biblioteca para manipular imágenes Netpbm',
    ext_modules=ext_modules,
)