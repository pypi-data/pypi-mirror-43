from setuptools import setup, find_packages

packages = [package for package in find_packages()]

setup(
  name='twsecli',
  packages=packages,
  version='0.6.2',
  description='TWSE unofficial command-line interface',
  long_description=open('README.md', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author='Hans Liu',
  author_email='hansliu.tw@gmail.com',
  url='https://github.com/hansliu/twsecli',
  keywords=['twse'],
  python_requires='>=3',
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
  entry_points={
    'console_scripts': [
      'twsecli=twsecli.cli:cli',
    ],
  }
)
