import os
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    reqs = f.read().splitlines()
    
print(reqs)
VERSION = os.getenv('PACKAGE_VERSION', 'v0.0.1')[1:]

setup(
    name='vi_nlp_core',
    version='1.1.3',
    description='vi-core-nlp is a library that supports Vietnamese NER by pattern matching .',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='https://github.com/demdecuong/vi-core-nlp/tree/master',
    packages=find_packages(),
    author='minhnp et al.',
    author_email='nguyenphucminh2804@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    install_requires=reqs,
    keywords='vi_nlp_core',
    python_requires='>=3.6',
    py_modules=['vi_nlp_core'],

)