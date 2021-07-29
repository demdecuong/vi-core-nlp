import os
from setuptools import setup, find_packages
from os import path

try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.download import PipSession
        from pip.req import parse_requirements

long_description = ''

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
try:
    reqs = [str(ir.req) for ir in install_reqs]
except:
    reqs = [str(ir.requirement) for ir in install_reqs]

VERSION = os.getenv('PACKAGE_VERSION', 'v0.0.1')[1:]

setup(
    name='vi_nlp_core',
    version='0.2',
    description='VMA-NLU is a library to implement NLU component in virtual medical assistant.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='https://github.com/demdecuong/NER_Extractor/tree/main',
    packages=find_packages(),
    author='minhnp',
    author_email='nguyenphucminh2804@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    install_requires=reqs,
    keywords='vi_nlp_core',
    python_requires='>=3.6',
    py_modules=['vi_nlp_core'],

)