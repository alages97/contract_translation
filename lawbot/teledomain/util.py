import os
import sys
import time
import logging
#import win32api
import subprocess
import shutil
from pathlib import Path
import getpass


PATH_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_DIR = r"%s" % PATH_DIR
OUTPUT_DIR = os.path.join(PATH_DIR, "./toTransfer/")
LOG_DIR = os.path.join(PATH_DIR, "./teleLogs/")
MOVE_DIR = os.path.join(PATH_DIR,"./testMoveDir/")

# Generate directories if not found
if not os.path.exists(MOVE_DIR):
    os.mkdir(MOVE_DIR)
    print("Made DIR %s" % MOVE_DIR)
    logging.info('util: Made DIR %s' % MOVE_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
    print("Made DIR %s" % OUTPUT_DIR)
    logging.info('util: Made DIR %s' % OUTPUT_DIR)
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
    print("Made DIR %s" % LOG_DIR)
    logging.info('util: Made DIR %s' % LOG_DIR)

def replaceMultiple(mainString, toBeReplaced, newString):
    for elem in toBeReplaced:
        if elem in mainString:
            if elem in "<>-:":
                newString =""
            mainString = mainString.replace(elem,newString)
    return mainString

def moveFolder(source,destination):
    listsource = os.listdir(source)
    print("Moving files: " + str(listsource))
    for name in listsource:
        if name == "System Volume Information":
            continue
        else :
            logging.info('util: Moving file: %s' % name + ' to '+ destination)
            #Use commandshell for windows, and moveFiles for linux
            #CommandShell(OUTPUT_DIR + name,destination)
            print(OUTPUT_DIR+name)
            moveFiles(OUTPUT_DIR+name,destination+"/"+name)


def numOfDir(source):
    d = os.listdir(source)
    return len(d)

def removeFilesFromFolder():
    folder = OUTPUT_DIR
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info('util: Removing file: %s' % file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def removeFiles():
    files = glob.glob(OUTPUT_DIR)
    for f in files:
        logging.info('util: Removing file: %s' % f)
        os.remove(f)


def CommandShell(folder,destination):
    folder = '"'+folder+'"'
    destination = '"'+destination+'"'
    subprocess.Popen(
        [
            r"C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe",
            "-ExecutionPolicy",
            "Unrestricted",
            ("Move-Item -Path %s -Destination %s"% (folder,destination)),
        ]
    )

def moveFiles(folder,destination):
    #os.rename(folder,destination)
    shutil.move(folder,destination)
    #os.replace(folder,destination)

def SearchMasterDrive():
    #following code for windows, comment out the below LINUX code when using windows
    #WINDOWS
    # drives = win32api.GetLogicalDriveStrings()
    # drives = drives.split('\000')[:-1]
    # for drive in drives:
    #     driveDetails = win32api.GetVolumeInformation(drive)
    #     driveName = driveDetails[0]
    #     if "MASTER" not in driveName:
    #         MOVE_DIR = os.path.join(PATH_DIR,"./testMoveDir/")
    #         if not os.path.exists(MOVE_DIR):
    #             os.makedirs(MOVE_DIR)
    #             logging.info('main: Could not find Master drive, moving files here instead: ' + MOVE_DIR)
    #         continue
    #     else:
    #         MOVE_DIR = drive
    #         print("Master drive found at  %s " % (drive))
    #         break
    # return MOVE_DIR

    #LINUX
    username = getpass.getuser()
    masterPath = '/media/'+username+'/MASTER'
    if not os.path.exists(masterPath):
        MOVE_DIR = os.path.join(PATH_DIR,"./testMoveDir/")
        if not os.path.exists(MOVE_DIR):
            os.makedirs(MOVE_DIR)
            logging.info('main: Could not find Master drive, moving files here instead: ' + MOVE_DIR)
    else :  
        print("Master drive found at %s " % (masterPath))
        MOVE_DIR = masterPath
    return MOVE_DIR



