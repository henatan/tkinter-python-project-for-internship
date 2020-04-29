import argparse, os, sys, datetime, subprocess, shutil
from _winreg import OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx, CloseKey

import pip._vendor.distlib.compat

ltssmBtn ='LTSSM'
LTSSM_Location = "."
selectedBtn= ''

def lounchLTSSMTests():
    with open('C:\TestSuite\LTSSM\LTSSM.txt', 'r')as f:
        list = []
        subTest=1
        for i in f:
            list.append(i.split('::'))
        for x in list:
            #print str(subTest) + " - " + x[1]
            subTest=subTest+1


def get_id():
    return subprocess.Popen('dmidecode.exe -s system-uuid'.split())

def runLTSSM():

    if selectedBtn == ltssmBtn:
        allTestsBtn = 'All Tests'
        print 'please select from the following tests or click all ' + '\n'
        print lounchLTSSMTests()
        print '9 - ' + allTestsBtn + '\n'
        subTest = pip._vendor.distlib.compat.raw_input('please select a sub test - ')
        count = pip._vendor.distlib.compat.raw_input('please enter how many times you want to run the test - ')
        while ( count!=0):
            if subTest == '1' or subTest == '9':
                print "\n\n=================  Running linkRetrain test..  =================\n"
                linkRetrain = os.path.join(LTSSM_Location,
                                           "LTSSMtool.exe linkRetrain {0} [{1},{2},{3}]".format(count, getBDF(DevId), 4,
                                                                                                4))
                cmd_out = os.system(linkRetrain)
                count= count-1
    else:
        print 'nothing'


print ' 1- LTSSM \n 2- IO Bandwidth \n 3- Data Integrity \n 4- RAID \n 5- PTC'
selectedOption= pip._vendor.distlib.compat.raw_input('please select a test - ')
print selectedOption
if selectedOption=='1':
    selectedBtn= 'LTSSM'
    runLTSSM()
elif selectedOption == 2:
    selectedBtn='IO Bandwidth'
elif selectedOption == 3:
    selectedBtn='Data Integrity'
elif selectedOption == 4:
    selectedBtn='RAID'
elif selectedOption == 5:
    selectedBtn='PTC'









