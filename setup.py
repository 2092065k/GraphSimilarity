from setuptools import setup, find_packages

setup(name='graphSimilarity',
      version='0.1.0',
      description='Graph Distance Measures and Clustering',
      author='Ivan Kyosev',
      author_email='2092065k@student.gla.ac.uk',
      license='GPL',
      install_requires=['numpy',
                        'matplotlib',
                        'networkx',
                        'scipy',
                        'scikit_learn'
                        ],
      package_data={'graphSimilarity': ['README.md']},
      packages=find_packages())
