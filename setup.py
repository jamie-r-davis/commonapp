import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='commonapp',
    version='0.0.2',
    author='Jamie Davis',
    author_email='jamjam@umich.edu',
    description='Interface for CommonApp Control Center',
    install_requires=[
        'beautifulsoup4',
        'requests'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jamie-r-davis/commonapp',
    packages=setuptools.find_packages()
)
