from setuptools import setup

setup(name='date_simple',
      version='0.1',
      description='Wrapper module which provides a simplified interface to a few of the date functions of the datetime module.',
      url='https://github.com/rcristal/nyu_advanced_python',
      author='Rexford Cristal',
      author_email='rexford.cristal@gmail.com',
      license='MIT',
      packages=['date_simple'],
      install_requires=[ ],
      test_suite='pytest',
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False)
