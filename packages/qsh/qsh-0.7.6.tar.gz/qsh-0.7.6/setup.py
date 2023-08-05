from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name='qsh',
    version='0.7.6',
    packages=find_packages(),
    url='https://github.com/nethask/qsh',
    author='Artyom Knyazev',
    author_email='nethask@gmail.com',
    license='MIT',
    setup_requires=[
        'cython'
    ],
    install_requires=[
        'python-dateutil',
    ],
    ext_modules=cythonize("qsh/*.py")
)
