from setuptools import setup, find_packages

setup(
    name='checkMyApp',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/flaunderg/checkMyApp',
    license='MIT',
    author='Daniel gur',
    author_email='dgur@outbrain.com',
    description='Tool for building python setup files.',
    install_requires=['check_manifest==0.37', 'pyflakes==2.1.0'],
    classifiers=["Operating System :: POSIX :: Linux",
                 "Intended Audience :: Developers",
                 "Topic :: Software Development :: Build Tools",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7"],
    entry_points={
        'console_scripts': [
            'checkMyApp = checkMyApp.checkMyApp:main'
        ]
    }
)
