from setuptools import setup, find_packages
import os

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='aioroku',
    version='0.0.2',
    description='Asynchronus client for the Roku media player',
    long_description=readme,
    author='Adam Garcia',
    author_email='garciadam@gmail.com',
    url='https://gitlab.com/pancho-villa/aioroku',
    packages=find_packages(),
    install_requires=[
        'aiohttp'
    ],
    license='BSD License',
    platforms=["any"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
