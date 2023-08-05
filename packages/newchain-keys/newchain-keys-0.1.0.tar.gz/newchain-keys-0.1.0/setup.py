#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)


deps = {
    'newchain-keys': [
        "eth-utils>=1.3.0,<2.0.0",
    ],
    'test': [
        'pytest==3.2.2',
        'hypothesis==3.30.0',
        "eth-hash[pysha3];implementation_name=='cpython'",
        "eth-hash[pycryptodome];implementation_name=='pypy'",
    ],
    'lint': [
        'flake8==3.0.4',
        'mypy<0.600',
    ],
    'dev': [
        'tox==2.7.0',
        'bumpversion==0.5.3',
        'twine',
    ],
}

deps['dev'] = (
    deps['dev'] +
    deps['newchain-keys'] +
    deps['lint'] +
    deps['test']
)

print(deps)

setup(
    name='newchain-keys',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.1.0',
    description="""Common API for NewChain key operations.""",
    long_description_markdown_filename='README.md',
    author='Xia Wu',
    author_email='xiawu@zeuux.org',
    url='https://github.com/xiawu/newchain-keys-py',
    include_package_data=True,
    setup_requires=['setuptools-markdown'],
    install_requires=deps['newchain-keys'],
    py_modules=['newchain_keys'],
    extras_require=deps,
    license="MIT",
    zip_safe=False,
    package_data={'newchain-keys': ['py.typed']},
    keywords='newchain',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
