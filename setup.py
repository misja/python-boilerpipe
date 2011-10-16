import os
import fnmatch
import urllib
import tarfile
from setuptools import setup, find_packages

__version__ = '1.2.0'

def getjars(package, rootdir):
    base   = "boilerpipe-%s/" % __version__
    jar    = "boilerpipe-%s.jar" % __version__
    url    = "http://boilerpipe.googlecode.com/files/boilerpipe-%s-bin.tar.gz" % __version__
    
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
      packages = find_packages('src'),
      package_dir = {'':'src'},
      install_requires = ['jpype', 'chardet'],
      package_data = {
          'boilerpipe': package_data('boilerpipe')
      },
      author = "Misja Hoebe",
      author_email = "misja.hoebe@gmail.com",
      description = "Python interface to Boilerpipe, Boilerplate Removal and Fulltext Extraction from HTML pages"
)
