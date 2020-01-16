import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-tracks',
    version='0.0.1',
    description='Manage your music tracks',
    long_description=read('README.md'),
    license='GPL',
    author='Ingo Fischer',
    author_email='mail@ingofischer.de',
    url='https://github.com/ifischer/django-tracks-api',
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    install_requires=[
        'Django',
        'djangorestframework',
        'mediafile',
        'mutagen',
    ],
)
