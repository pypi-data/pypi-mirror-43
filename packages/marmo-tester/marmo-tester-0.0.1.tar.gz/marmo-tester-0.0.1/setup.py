from setuptools import find_packages, setup


setup(
    name='marmo-tester',
    
    version="0.0.1",
    
    description='Marmo wallet Python SDK',
    
    author='Agustin Aguilar',
    
    author_email='agusxrun@gmail.com',
    
    url='',
    
    packages=find_packages(exclude=('tests',)),

    install_requires=[
        "marmopy"
    ],

    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],    
)
