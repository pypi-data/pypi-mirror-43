#!/usr/bin/env python3

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""
from dhunter.core.const import Const
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
        name=Const.APP_NAME,
        version=Const.APP_VERSION,
        packages=find_packages(),

        install_requires=[
            'argparse>=1.4.0',
        ],
        python_requires='>=3.6',
        entry_points={
            'console_scripts': [
                'dscan = dhunter.scanner.scanner:Scanner.start',
                'dhunt = dhunter.hunter.hunter:Hunter.start',
            ],
        },

        author="Marcin Orlowski",
        author_email="mail@marcinOrlowski.com",
        description="The hunter - fast and easy file duplicate finder utility.",
        long_description=readme,
        long_description_content_type="text/markdown",
        url='https://github.com/MarcinOrlowski/duplicate-hunter',
        keywords="file duplicates deduplicate",
        project_urls={
            "Bug Tracker": "https://github.com/MarcinOrlowski/dhunter/issues",
            "Documentation": "https://github.com/MarcinOrlowski/dhunter/",
            "Source Code": "https://github.com/MarcinOrlowski/dhunter/",
        },
        # https://choosealicense.com/
        license="MIT License",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)
