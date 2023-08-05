import setuptools

setuptools.setup(
    name='rbk',
    version='0.0.1',
    author='Richard Keller',
    author_email='',
    url='https://github.com/rbk/pyrbk',
    description='MySQL class wrapper for PyMySQL',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages()
)


# python3 -m twine upload --repository pypi dist/*
