#! /usr/bin/env python

from optparse import OptionParser
import sys
import os
import subprocess
import time
import shutil
import glob
import tarfile

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

def copyFiles(source, version):
    (options, args)=getOptions().parse_args()
    for file in glob.glob(source + '*_' + version + '_*.gz'):
#      print "contains logs: " + str(file.find("logs"))
#      print "contains rlx: " + str(file.find("rlx"))
#      print "contains artifacts: " + str(file.find("artifacts"))
      if ((file.find("logs") > 0) or ((file.find("rlx") > 0) and (file.find("artifacts") > 0))): 
        print "Copy " + file + " to " + options.outputdir        
#        shutil.copy(file, options.outputdir)

def copyAllFiles():
    (options, args)=getOptions().parse_args()
    print "Copy files from builddrop to " + options.outputdir
    
    source = "../../.gvfs//build_output on rkams889/Roche.DP.NewGen/IS/pkg_00000163_ISNewGen/"
    copyFiles(source, options.icversion)
    
    source = "../../.gvfs//build_output on rkams889/Roche.DP.NewGen/IS/csm_00000136_SamplePrepProcessor/"
    copyFiles(source, options.sppversion)

    source = "../../.gvfs//build_output on rkams889/Roche.DP.NewGen/IS/csm_00000202_SampleTransferProcessor/"
    copyFiles(source, options.stpversion)

    source = "../../.gvfs//build_output on rkams889/Roche.DP.NewGen/IS/csm_00000227_ADProcessor/"
    copyFiles(source, options.adpversion)
    

def unpackTAR():
    print "Unpack the tar.gz"
    (options, args)=getOptions().parse_args()
    for file in glob.glob(options.outputdir + "*"):
        print "unpack " + file
        TarFile = tarfile.open(file, 'r')
        TarFile.extractall(file)

def deleteOutputFolder():
    (options, args)=getOptions().parse_args()
    print "Delete *.gz files from " + options.outputdir
    for file in glob.glob(options.outputdir + "*.gz"):
      os.remove(file)

def main():
    deleteOutputFolder()
    copyAllFiles()
#    unpackTAR()

if __name__ == '__main__':
    sys.exit(main())
