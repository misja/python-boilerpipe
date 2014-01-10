import os
import imp
import jpype

print "jpype.isJVMStarted()  ",jpype.isJVMStarted()
if jpype.isJVMStarted() != True:
    jars = []
    for top, dirs, files in os.walk(imp.find_module('boilerpipe')[1]+'/data'):
        for nm in files:       
            jars.append(os.path.join(top, nm))
    print "---->",jpype.startJVM(jpype.getDefaultJVMPath()),"==> path ",jpype.getDefaultJVMPath()        
    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % os.pathsep.join(jars))
