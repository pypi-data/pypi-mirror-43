"""
- Upload SMNet to pypi
```
python setup.py sdist 
twine upload dist/*
rm -r dist
rm -r smnet.egg-info
```
"""

from setuptools import find_packages, setup

setup(
    name = 'smnet',
    version = '1.0.0',
    packages = find_packages(),
    install_requires = [
        'numpy>=1.16.1',
        'logging>=0.4.9.6',
    ],
    author = 'smarsu',
    author_email = 'smarsu@foxmail.com',
    url = 'https://github.com/smarsuuuuuuu/SMNet',
)
