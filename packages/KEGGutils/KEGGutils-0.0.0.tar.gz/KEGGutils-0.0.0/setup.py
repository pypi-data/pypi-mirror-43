import os
from setuptools import setup

# view filename
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()



__version__ = exec(open('KEGGutils/_version.py').read())


setup(
    name = "KEGGutils",
    version =__version__,
    author = "Filippo Castelli",
    author_email = "filippocastelli42@gmail.com",
    description = ("Simple utils to work with KEGG data on NetworkX"),
    license = "Unlicense",
    keywords = "KEGG networkx utils",
    url = "https://github.com/filippocastelli/KEGGutils",
    packages=['KEGGutils'],
    install_requires=['networkx', 'requests', 'matplotlib', 'os'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: Public Domain",
    ],
)