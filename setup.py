from setuptools import setup

setup(name='temoatools',
      version='0.1',
      description='Modeling tools to support electric sector analyses in Temoa',
      url='https://github.com/EnergyModels/temoatools',
      author='Jeff Bennett',
      author_email='jab6ft@virginia.edu',
      license='MIT',
      packages=['temoatools'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['pandas','numpy'])