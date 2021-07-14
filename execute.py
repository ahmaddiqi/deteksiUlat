import sys
nameFile = 'GUI Pest detector.py'
if((sys.version_info[0] == 3)) :
    exec(open(nameFile).read())
else :
    execfile(nameFile)