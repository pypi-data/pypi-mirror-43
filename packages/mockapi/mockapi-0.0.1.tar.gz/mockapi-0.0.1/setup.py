import setuptools
from mockapi import __version__, __doc__

setuptools.setup(
    name = 'mockapi',
    version = __version__,
    packages = setuptools.find_packages(),

    author="Sylvan LE DEUNFF",
    author_email="sledeunf@gmail.com",

    description="Package to mock a REST API.",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",

    

    entry_points = {
        'console_scripts': [
            'mockapi = mockapi.__main__:mock'
        ]
    })
