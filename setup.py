from setuptools import setup

setup(name='temoatools',
      version='1.0.0',
      description='Modeling tools to support electric sector analyses in Temoa',
      url='https://github.com/EnergyModels/temoatools',
      author='Jeff Bennett',
      author_email='jab6ft@virginia.edu',
      packages=['temoatools'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['pandas', 'numpy', 'sqlite3', 'matplotlib', 'seaborn','joblib'])