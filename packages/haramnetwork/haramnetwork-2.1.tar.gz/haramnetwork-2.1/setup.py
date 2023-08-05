from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='haramnetwork',
    version='2.1',
    scripts=['chunky_boy.py','main_func.py','netutils.py','trackclient.py','tracker.py','torrent.libr'] ,
    author='FOMK',
    author_email='kriskuliv@gmail.com',
    description='download the halal staff for free with no registration',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/UJM-INFO/2019-net-b',
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['numpy', 'dill'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
