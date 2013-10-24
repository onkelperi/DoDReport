#! /usr/bin/env python

from optparse import OptionParser
import sys
import os
import subprocess
import time
import shutil
import glob
import tarfile
import re



def getOptions():
    currentDir = (os.path.dirname( os.path.realpath( __file__ ) ))
    parser = OptionParser(usage="usage: %prog [options]\n\n" \
        "It helps to create the painful DoD report or at least some part of it.", version="%prog 1.00")
    _add = parser.add_option
    _add ("-v", "--icversion",      action="store",        dest="icversion",     default="0.00.00",                      help="The IC version in the format V.II.SS")
    _add ("-a", "--adpversion",     action="store",        dest="adpversion",    default="0.00.00",                      help="Version of ADProcessor in the format V.II.SS")
    _add ("-s", "--stpversion",     action="store",        dest="stpversion",    default="0.00.00",                      help="Version of SampleTransferProcessor in the format V.II.SS")
    _add ("-p", "--sppversion",     action="store",        dest="sppversion",    default="0.00.00",                      help="Version of SamplePrepProcessor in the format V.II.SS")
    _add ("-o", "--output",         action="store",        dest="outputdir",     default=os.getenv("HOME") + "/Desktop", help="Target folder to copy the release to.")
    return parser


class TargetFolderList():
    (options, args)=getOptions().parse_args()
    BuildLogs = "BuildLogs_InstrumentControl_" + options.icversion
    UnitTestCoverage = "UnitTestCoverage_InstrumentControl_" + options.icversion
    UnitTestResults = "UnitTestResults_InstrumentControl_" + options.icversion
    Array = [BuildLogs,
             UnitTestCoverage,
             UnitTestResults]
    

def copyFiles(source, version):
    (options, args)=getOptions().parse_args()
    for file in glob.glob(source + '*_' + version + '_*.gz'):
      if (("logs" in file) or ("rlx" in file) and ("artifacts" in file)):
        print "Copy " + file + " to " + options.outputdir
        shutil.copy(file, options.outputdir)

def copyAllFiles():
    (options, args)=getOptions().parse_args()
    print "Copy files from builddrop to " + options.outputdir

#    source = "../../.gvfs//build_output on rkams889/Roche.DP.NewGen/IS/pkg_00000163_ISNewGen/"
#    copyFiles(source, options.icversion)

    source = "../../.gvfs//build_output on rkams889/Roche.DP.NewGen/IS/csm_00000136_SamplePrepProcessor/"
    copyFiles(source, options.sppversion)

    source = "../../.gvfs//build_output on rkams889/Roche.DP.NewGen/IS/csm_00000202_SampleTransferProcessor/"
    copyFiles(source, options.stpversion)

    source = "../../.gvfs//build_output on rkams889/Roche.DP.NewGen/IS/csm_00000227_ADProcessor/"
    copyFiles(source, options.adpversion)


def unpackTAR():
    (options, args)=getOptions().parse_args()
    UnpackFolder = options.outputdir + "unpacked"
    CreateFolderIfNotExists(UnpackFolder)
    unpackArtifacts(options.outputdir, UnpackFolder)

def unpackArtifacts(TarPath, UnpackFolder):
    print "Unpack the artifacts.tar.gz"
    FileList = glob.glob(TarPath + "*_artifacts.tar.gz")
    for file in FileList:
        print "unpack " + file
        TarFile = tarfile.open(file)
        TarFile.extractall(UnpackFolder)
        TarFile.close()

def copyLogArchived():
    (options, args)=getOptions().parse_args()
    LogsFolder = options.outputdir +  "BuildLogs_InstrumentControl_" + options.icversion
    CreateFolderIfNotExists(LogsFolder)
    FileList = glob.glob(options.outputdir + "*_logs.tar.gz")
    for file in FileList:
        print "copy " + file + " to " + LogsFolder
        shutil.copy(file, LogsFolder)
    
def copyCovHtml():
    (options, args)=getOptions().parse_args()
    CovHTMLFolder = options.outputdir + "UnitTestCoverage_InstrumentControl_" + options.icversion
    CreateFolderIfNotExists(CovHTMLFolder)
    FolderList = os.listdir(options.outputdir + "unpacked/")
    for folder in FolderList:
        Source = options.outputdir + "unpacked/" + folder + "/CovHtml"
        FolderSubSet = re.findall("[^_]+", folder)
        Destination = CovHTMLFolder + "/" + FolderSubSet[2] + "_" + FolderSubSet[3] + "_UnitTestCoverageReport"
        print "folder: " + folder + ", from Source: " + Source + ", To Destination: " + Destination
        shutil.copytree(Source, Destination)
    
def copyTestResultPDF():
    (options, args)=getOptions().parse_args()
    LogsFolder = options.outputdir + "UnitTestResults_InstrumentControl_" + options.icversion
    CreateFolderIfNotExists(LogsFolder)
    FolderList = os.listdir(options.outputdir + "unpacked/")
    for folder in FolderList:
        Source = options.outputdir + "unpacked/" + folder + "/TestResults/Release/"
        Destination = LogsFolder
        print "copy *.pdf from " + Source + " to " + Destination
        FileList = glob.glob(Source + "*.pdf")
        for file in FileList:
            print "copy " + file + " to " + Destination
            shutil.copy(file, Destination)

def deleteUnusedFilesAndFolders():
    (options, args)=getOptions().parse_args()
    deleteOutputFolder()
    print "Delete unpacked folder from " + options.outputdir
    shutil.rmtree(options.outputdir + "unpacked")

def deleteOutputFolder():
    (options, args)=getOptions().parse_args()
    print "Delete *.gz files from " + options.outputdir
    for file in glob.glob(options.outputdir + "*.gz"):
        os.remove(file)

def CreateFolderIfNotExists(Folder):
    if (os.path.exists(Folder)):
        print "folder " + Folder + " does already exists. Delete before create new"
        shutil.rmtree(Folder)
    print "create folder " + Folder
    os.makedirs(Folder)

def main():
    deleteOutputFolder()
    copyAllFiles()
    unpackTAR()
    copyLogArchived()
    copyCovHtml()    
    copyTestResultPDF()
    deleteUnusedFilesAndFolders()

if __name__ == '__main__':
    sys.exit(main())
