#!/usr/bin/env python3

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='space-translation-util',
    version='0.0.7',
    author='Roman Akopov',
    author_email='roman.akopovi@space.ge',
    description='Space Translation Utility',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SpaceBank/space-translation-util',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'colorama>=0.4.1',
        'google-api-python-client>=1.7.8',
        'google-auth-httplib2>=0.0.3',
        'google-auth-oauthlib>=0.2.0',
    ],
    entry_points={
        'console_scripts': [
            'space-translation-util=space_translation_util:main',
        ],
    },
)

