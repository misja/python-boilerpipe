import os
import fnmatch
import urllib
import tarfile
from setuptools import setup, find_packages

__version__ = '1.2.0.0' # Maintain an extra version digit for enhancements to this library
__boilerpipe_version__ = '1.2.0'

def getjars(package, rootdir):
    base   = "boilerpipe-%s/" % __boilerpipe_version__
    jar    = "boilerpipe-%s.jar" % __boilerpipe_version__
    url    = "http://boilerpipe.googlecode.com/files/boilerpipe-%s-bin.tar.gz" % __boilerpipe_version__
    
    if os.path.exists(rootdir+'/'+base):
        return
    
    handle = tarfile.open(urllib.urlretrieve(url)[0], mode='r:gz')
    files  = [handle.getmember(name) for name in handle.getnames() if name == base+jar or name.startswith(base+'lib')]
    
    handle.extractall(rootdir, files)

def package_data(package, **kwargs):
    fileList = []
    rootdir  = "src/%s/data" % package

    getjars(package, rootdir)
    
    exclude=['']
    if kwargs and kwargs['exclude']:
        exclude=kwargs['exclude']
    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            for pattern in exclude:
                if not fnmatch.fnmatch(file, pattern):
                    path = root.replace(rootdir,'data')
                    fileList.append(os.path.join(path,file))
    return fileList

setup(
      name = 'boilerpipe',
      version = __version__,
      packages = ['boilerpipe'],
      package_dir = {'':'src'},
      install_requires = ['JPype1', 'chardet'],
      package_data = {
          'boilerpipe': package_data('boilerpipe')
      },
      zip_safe = False,
      author = "Misja Hoebe",
      author_email = "misja.hoebe@gmail.com",
      maintainer = 'Matthew Russell',
      maintainer_email = 'ptwobrussell@gmail.com',
      url = 'https://github.com/ptwobrussell/python-boilerpipe/',
      description = "Python interface to Boilerpipe v%s (Java) - Boilerplate Removal and Fulltext Extraction from HTML pages" % (__boilerpipe_version__,),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Natural Language :: English',
      ],
      keywords='boilerpipe'
)
