from distutils.core import setup
import setuptools
import sys


_version = '0.1'
_packages = ['lexer']

_short_description = "Pygments lexer for finesse kat files."

_install_requires = [
    'pygments>=2'
]

setup(
    name='pygments-finesse',
    author='Philip Jones',
    url='https://github.com/philj56/pygments-finesse',
    description=_short_description,
    version=_version,
    packages=_packages,
    install_requires=_install_requires,
    keywords='pygments syntax highlighting',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'pygments.lexers': [
            'finesse = lexer:FinesseLexer',
        ]
    }
)
