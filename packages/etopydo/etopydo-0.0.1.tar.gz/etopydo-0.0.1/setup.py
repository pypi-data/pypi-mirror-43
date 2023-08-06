import codecs

import os

import setuptools 
with open("README.md", "r") as fh:
    long_description = fh.read()
#import find_packages, setup

_HERE = os.path.abspath(os.path.dirname(__file__))



def read(*parts):

    # intentionally *not* adding an encoding option to open

    return codecs.open(os.path.join(_HERE, *parts), 'r').read()



def find_version(*file_paths):

    version_file = read(*file_paths)

    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",

                              version_file, re.M)

    if version_match:

        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

WATCHDOG = 'watchdog >= 0.8.3'
ICALENDAR = 'icalendar'


setuptools.setup(

    name="etopydo",

    version="0.0.1",

    description="A powerful todo.txt application for the console",

    author="Eddie",

    author_email="eddie@example.org",

    url="https://www.example.org",

    install_requires=[

        'arrow >= 0.7.0',

    ],

    extras_require={

        ':sys_platform=="win32"': ['colorama>=0.2.5'],

        ':python_version=="3.2"': ['backports.shutil_get_terminal_size>=1.0.0'],

        'columns': ['urwid >= 1.3.0', WATCHDOG],
        'ical': [ICALENDAR],

        'prompt': ['prompt_toolkit >= 0.53', WATCHDOG],

        'test': ['coverage>=4.3', 'freezegun', 'green', ICALENDAR, 'pylint>=1.7.1'],

        'test:python_version=="3.2"': ['mock'],

    },

    entry_points={

        'console_scripts': ['etopydo=etopydo.ui.UILoader:main'],

    },

    classifiers=[

        "Environment :: Console",

        "Intended Audience :: End Users/Desktop",

        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",

        "Natural Language :: English",

        "Programming Language :: Python :: 3.2",

        "Programming Language :: Python :: 3.3",

        "Programming Language :: Python :: 3.4",

        "Programming Language :: Python :: 3.5",

        "Programming Language :: Python :: Implementation :: CPython",

        "Programming Language :: Python :: Implementation :: PyPy",

        "Topic :: Utilities",

    ],

    long_description="""\This is just eddie dicking around with topydo.
	I am very new to programming and make no garuntees of anything working.""",


    test_suite="test",

)
