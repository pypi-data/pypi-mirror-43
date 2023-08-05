from setuptools import setup, find_packages

with open('README.md') as readme_file:
    long_description = readme_file.read()
with open('LICENSE.txt') as license_file:
    license = license_file.read()

setup(
    name='tagtomarkdown',
    version='0.2.5',
    description='Python3 markdown extension for converting tags to markdown table',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['markdown'],
    py_modules=['tagtomarkdown'],
    #package_dir={'tagtomarkdown': 'transform'},
    #packages=['transform'],
    #packages=find_packages('transform'),
    #packages=find_packages(exclude=('test')),
    #include_package_data=True,
    #package_data={'tagtomarkdown': 'test_data/produceHtml.py', 'README.txt'},
    #data_files=[('testfiles', ['test_data/produceHtml.py', 'README.txt'])],
    author='Christian Hauris Sorensen',
    author_email='chrhauris@hotmail.com',
    url='http://test.pypi.org/pypi/tagtomarkdown/',
    license=license,
    entry_points={
      'markdown.extensions': ['tagtomarkdown = tagtomarkdown:TableTagExtension']
    }
)