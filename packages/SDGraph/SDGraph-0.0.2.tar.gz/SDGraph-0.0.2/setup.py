import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()


setuptools.setup(
  name="SDGraph",
  version="0.0.2",
  author="Cha Chen",
  author_email="chencha92111@gmail.com",
  description="A simple jedi based python3 dependency analysis tool",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/jam-world/py3_dependency_graph",
  packages=setuptools.find_packages(),
  scripts=['bin/SDGraph'],
  install_requires=[
    'GitPython', 'jedi', 'networkx'
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
