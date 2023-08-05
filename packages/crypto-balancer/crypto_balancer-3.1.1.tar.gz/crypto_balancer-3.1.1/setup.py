import os
from setuptools import setup

base_path = os.path.dirname(__file__)
with open(os.path.join(base_path, "README.md"), encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(name='crypto_balancer',
      version='3.1.1',
      packages=['crypto_balancer'],
      entry_points={
          'console_scripts': [
              'crypto_balancer = crypto_balancer.main:main'
          ]
      },
      license='MIT',
      description = 'A tool to automatically balance cryptocurrency portfolios',
      long_description=readme,
      long_description_content_type='text/markdown',
      author = 'Matt Hamilton',
      author_email = 'mh@quernus.co.uk',
      url = 'https://github.com/hammertoe/crypto_balancer',
      download_url = 'https://github.com/hammertoe/crypto_balancer/archive/3.1.1.tar.gz',
      keywords = ['cryptocurrency', 'portfolio', 'xrp', 'ethereum', 'bitcoin', 'btc', 'eth'],
      install_requires=[
          'ccxt',
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Financial and Insurance Industry',
          'Topic :: Office/Business :: Financial :: Investment',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
      )
