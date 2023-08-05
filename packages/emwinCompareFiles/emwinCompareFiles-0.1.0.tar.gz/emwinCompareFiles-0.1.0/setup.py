import setuptools

setuptools.setup(
    name='emwinCompareFiles',
    version='0.1.0',
    author='Katie DAdamo',
    author_email='katherine.dadamo@noaa.gov',
    description='EMWIN Latency Comparison.',
    url='https://pypi.org/project/emwinCompareFiles/',
    packages=setuptools.find_packages(),
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.1",
        "caldav == 0.1.4",
    ],
)
