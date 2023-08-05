from setuptools import setup
import os

PATH = os.getcwd()
print(PATH)

__version__ = '0.18.47'

setup(
    name='shakespear',
    packages=['shakespear'],
    package_dir={'shakespear': 'writers'},
    version=__version__,  # noqa
    description='XML-esque text from python',
    author='Richard Stoeffel',
    url='https://github.com/Price47/Shakespear',
    author_email="richardstoeffel47@gmail.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
