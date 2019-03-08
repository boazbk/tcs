#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='pygments-mdcpp',
    description='Pygments lexer for object-oriented molecular dynamics C++.',
    long_description=open('README.md').read(),
    keywords='pygments molecular-dynamics cpp c++ lexer',

    packages=find_packages(),
    install_requires=['pygments >= 1.4'],

    entry_points='''[pygments.lexers]
                    mdcpp=pygments_mdcpp:MDCppLexer''',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
