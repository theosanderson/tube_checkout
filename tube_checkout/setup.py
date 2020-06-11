from setuptools import setup

setup(name='tube_checkout',
      version='0.1',
      description='Scan tube barcodes with OpenTrons',
      url='http://github.com/theosanderson/tubecheckout',
      author='Theo Sanderson',
      author_email='theo@theo.io',
      license='MIT',
      packages=['tube_checkout'],
      install_requires=[
          'opentrons==3.18.1',
      ],
      include_package_data=True,
      zip_safe=False)