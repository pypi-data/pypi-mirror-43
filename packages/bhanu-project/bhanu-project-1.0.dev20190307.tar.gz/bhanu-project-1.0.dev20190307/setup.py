from setuptools import setup,find_packages
import os

setup(
    name='bhanu-project',
    version='1.0',
    description='A sample Python project',
    long_description='long_description',
    packages=['bhanu-project'],
    #packages= find_packages(),
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    #url='https://gitlab.caratred.com/bhanuchander008/application',

    #packages=find_packages(),
    install_requires=[
        'flask',

    ],
classifiers=[

    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
],

)
