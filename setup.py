from setuptools import setup, find_packages

import gcm

version = gcm.VERSION

requires = [
    'Django>=1.7',
    'djangorestframework==3.1.3',
    'mock==1.0.1',
    'pytz==2015.4',
    'requests==2.7.0',
]

setup(
    name='django-gcm-android-ios',
    version=version,
    author='Hugo Brilhante',
    author_email='hugobrilhante@gmail.com',
    packages=find_packages(),
    license='MIT',
    description='Send a message using GCM HTTP connection server protocol',
    long_description=open('docs/index.rst').read(),
    url='https://github.com/hugobrilhante/django-gcm-android-ios',
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
