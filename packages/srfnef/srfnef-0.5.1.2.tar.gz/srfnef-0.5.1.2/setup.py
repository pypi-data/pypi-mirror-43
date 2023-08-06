from setuptools import setup, find_packages

setup(name = 'srfnef',
      version = '0.5.1.2',
      py_modules = ['srfnef'],
      description = 'Scalable Reconstruction Framework -- Not Enough Functions',
      author = 'Minghao Guo',
      author_email = 'mh.guo0111@gmail.com',
      license = 'Apache',
      # packages = ['srfnef'],
      packages = find_packages(),
      install_requires = [
          'scipy',
          'matplotlib',
          'typing',
          'h5py',
          'click',
          'numpy',
          'tqdm',
          'numba',
          'deepdish',
          'Click',
      ],
      zip_safe = False,
      entry_points = '''
        [console_scripts]
        srfnef=srfnef.app.cli:cli
      ''',
      )
