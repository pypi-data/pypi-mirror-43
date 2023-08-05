"""
установка пакета pybga, в папке с setup.py ->
pip3 install --upgrade .
"""

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pybga',
      version='0.6',
      description='useful to make pins into Altium component lib',
      long_description=long_description, 
      long_description_content_type='text/markdown',   
      author='Nikita Kuzin',
      author_email='getsense@yandex.ru',
      packages=['pybga'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freeware",
        "Operating System :: OS Independent",
      ],
      zip_safe=False
)
