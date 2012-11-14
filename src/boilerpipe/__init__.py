import os
import imp

jars = []
for top, dirs, files in os.walk(imp.find_module('boilerpipe')[1]+'/data'):
    for nm in files:
        if nm.lower().endswith('jar'):
            jars.append(os.path.join(top, nm))

os.putenv('CLASSPATH', os.pathsep.join(jars))