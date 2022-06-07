
from setuptools import setup, find_packages

setup(name='generateMsconvertConfig',
      version=0.1,
      author='Aaron Maurais',
      # url=
      packages=find_packages(),
      package_dir={'generateMsconvertConfig': 'src'},
      python_requires='>=3.8',
      install_requires=['pyopenms==2.7.0'],
      entry_points={'console_scripts': ['generateMsconvertConfig=src:main']}
)
