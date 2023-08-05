from setuptools import setup
from setuptools.command.test import test as TestCommand
import pyphoenix
import sys

setup(
    name="PyPhoenixS",
    version=1.0,
    python_requires='>3.6',
    description="Python interface to Phoenix",
    long_description="long_description",
    author="Karteek",
    author_email="karteek@coverfoxmail.com.com",
    license="Apache License, Version 2.0",
    packages=['pyphoenix'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Database :: Front-Ends",
    ],
    install_requires=[
        'future',
        'sqlalchemy',
        'phoenix',
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'phoenix = pyphoenix.sqlalchemy_phoenix:PhoenixDialect',
        ],
    }
)
