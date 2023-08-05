import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='teimc',
    version='1.0.0',
    author='Jay Bassan',
    author_email='jay.s.bassan@gmail.com',
    description='Functions for processing imaging mass cytometry data with\
    tellurium isotopes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jaybassan/teimc',
    keywords='imaging mass cytometry tellurium imc',
    packages=setuptools.find_packages(),
    classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
    ]
)
