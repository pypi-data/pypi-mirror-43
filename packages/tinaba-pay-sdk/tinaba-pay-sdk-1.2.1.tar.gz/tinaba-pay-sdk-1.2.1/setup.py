from distutils.core import setup
from setuptools import find_packages

SDKVERSION = '1.2.1'

requirements = ['voluptuous==0.10.5',
                'requests==2.18.4']

setup(name='tinaba-pay-sdk',
      version=SDKVERSION,
      packages=find_packages(),
      install_requires=requirements,
      description='A Python3 library to easily integrate your eCommerce website with the Tinaba system',
      author='MovEax srls',
      author_email='simone.bronzini@moveax.it',
      url='https://gitlab.com/tinaba-open/tinaba-pay-sdk-python',
      download_url='https://gitlab.com/tinaba-open/tinaba-pay-sdk-python/-/archive/1.2/tinaba-pay-sdk-python-{}.tar.gz'.format(SDKVERSION),
      python_requires='>=3',
      keywords=['tinaba', 'sdk', 'ecommerce'])
