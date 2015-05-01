#!/usr/bin/python

from __future__ import print_function
import os
import getopt
import sys
import time
from subprocess import PIPE, Popen


dirToSearch = os.getcwd()
delete = False
fileToCheck = ''
f = False


def isVideoFile(filePath):
    return (filePath[-3:] in ['avi', 'dat', 'mp4', 'mkv', 'vob'])


def shellquote(s):
    try:  # py3
        from shlex import quote
    except ImportError:  # py2
        from pipes import quote
    return quote(s)


def getLogFile():
    global f
    if not f:
        f = open('deleteVideoFileIfCorrypted_Output.txt', 'w')

    return f;

def writeToFile(string):
    getLogFile().write('%s\n' % string)


def handleCorryptedFile(filePath):
    writeToFile(filePath)
    if delete:
        os.remove(filePath)


def deleteVideoFileIfCorrypted(filePath):
    try:
        stdout, stderr = Popen('nice avconv -v error -i %s -f null ->&1' % shellquote(filePath), stdout=PIPE, stderr=PIPE, shell=True).communicate()
        if stderr or stdout:
            print('Stderr: %s' % stderr)
            print('stdout: %s' % stdout)
            print ("Delete file %s" % filePath)
            handleCorryptedFile(filePath)
    except Exception, e:
        print ('Delete file %s\n%s ' % (filePath, e))
        handleCorryptedFile(filePath)


def findAllVideoFilesInDir(dirToSearch):
    videoFiles = []
    if dirToSearch:
        print ("Searching %s..." % dirToSearch)
        for root, dirnames, filenames in os.walk(dirToSearch):
            videoFiles += [os.path.join(root, filename) for filename in filter(isVideoFile, filenames)]
    return filter(os.path.isfile, videoFiles)


def parseCommands(argv):
    global delete
    global fileToCheck
    try:
        opts, args = getopt.getopt(argv, "Di:o:", ["ifile=", "ofile="])
        for opt, arg in opts:
            if opt == '-D':
                print ('Deleting corrypted files')
                delete = True
            if opt == '-i':
                delete = True
                fileToCheck = arg
    except getopt.GetoptError:
        pass


def main(argv):
    parseCommands(argv)

    writeToFile(time.strftime("%c"))
    print(fileToCheck)

    if fileToCheck:
        videoFiles = [fileToCheck]
    else:
        videoFiles = findAllVideoFilesInDir(dirToSearch)
    numberOfVideos = len(videoFiles)

    for number, filePath in enumerate(videoFiles):
        print ("%d of %d: Scanning %s" % (number + 1, numberOfVideos, filePath))
        deleteVideoFileIfCorrypted(filePath)

    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
