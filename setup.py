import tarfile
from fnmatch import fnmatch
from os.path import basename, exists, dirname, abspath, join
from distutils.core import setup

try:
    from urllib import urlretrieve
except:
    from urllib.request import urlretrieve

__version__ = '1.3.0.0'
boilerpipe_version = '1.2.0'
DATAPATH = join(abspath(dirname((__file__))), 'src/boilerpipe/data')

def download_jars(datapath, version=boilerpipe_version):
    tgz_url = 'https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/boilerpipe/boilerpipe-{0}-bin.tar.gz'.format(version)
    tgz_name = basename(tgz_url)
    if not exists(tgz_name):
        urlretrieve(tgz_url, tgz_name)
    tar = tarfile.open(tgz_name, mode='r:gz')
    for tarinfo in tar.getmembers():
        if not fnmatch(tarinfo.name, '*.jar'):
            continue
        tar.extract(tarinfo, datapath)

download_jars(datapath=DATAPATH)

setup(
    name='boilerpipe',
    version=__version__,
    packages=['boilerpipe', 'boilerpipe.extract'],
    package_dir={'': 'src'},
    package_data={
        'boilerpipe': [
            'data/boilerpipe-{version}/boilerpipe-{version}.jar'.format(version=boilerpipe_version),
            'data/boilerpipe-{version}/lib/*.jar'.format(version=boilerpipe_version),
        ],
    },
    install_requires=[
        'JPype1',
        'chardet',
    ],
    author='Misja Hoebe',
    author_email='misja.hoebe@gmail.com',
    maintainer='Matthew Russell',
    maintainer_email='ptwobrussell@gmail.com',
    url='https://github.com/ptwobrussell/python-boilerpipe/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
    ],
    keywords='boilerpipe',
    license='Apache 2.0',
    description='Python interface to Boilerpipe, Boilerplate Removal and Fulltext Extraction from HTML pages'
)
