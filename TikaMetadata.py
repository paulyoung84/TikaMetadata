'''

Based on script by Peter May from British Library created on 17 Apr 2012, updated to Python 3 and added tika-app-1.18 batch processing to create json output, then tidy for processing of main script to collate json into single CSV

@author: Paul Young
@organization: The National Archives
@contact: paul.young@nationalarchives.gov.uk
'''

import csv
import json
import os
import sys
import subprocess
import shutil

## HEADINGS to ignore - columns/keywords in this set will be ignored
## helps prevent strange parsing outputs where one file's results split onto multiple rows
IGNORE = ['X-TIKA:content', 'X-TIKA:EXCEPTION:embedded_stream_exception','PCF1']

# Useful properties
#PROPS = ['Content-Type', 'Application-Name', 'creator', 'producer', 'Author', 'Content-Length', 'Page-Count', 'Revision-Number', 'Creation-Date', 'Last-Modified', 'Last-Save-Date', 'Last-Printed']

# CSV Headings
HEADINGS = ['Filename', 'Read TikaRunner Output']
#HEADINGS.extend(PROPS)      # add in the useful properties headings


def tikagrab(origdir): #batch process to run tika process to create json files
	command = "java -Xmx1024m -jar tika-app-1.19.jar -Jmx1024m -bc tika-batch-config.xml -J -m -i "+ '"' + origdir + '"' " -o "+ '"'+ JSONout + '"'
	subprocess.call(command, shell=True)
	
def __listFilesInDir(JSONout):
    """Lists all files (recursively) in the specified directory"""
    fileList = []
    for root, subFolders, files in os.walk(JSONout):
        #print (root, subFolders, files)
        for file in files:
            fileList.append(os.path.join(root, file))
    return fileList

def jsonclean(origdir): #tidies json files up for script remove [] brackets
    fileList = __listFilesInDir(JSONout)
	
    for filename in fileList:
    	try:
    		with open("\\\\?\\"+filename, 'r', encoding = "latin-1") as afile:
    			json = afile.read()
    			json = json.strip("[]")
    			json = json.replace("},{","}[[REMOVE]]")
    			json = json.replace("\\n", "\\\\n")
    			json = json.replace("\\\\\\n", "\\\\n")
    			json = json.split("[[REMOVE]]", 1)[0]
    		with open("\\\\?\\"+filename, 'w', encoding = "latin-1") as afile:
    			afile.write(json)
    	except:
            pass
            print("Unable to scan file "+filename)
			 
def processdir(origdir):
    """Aggregates all JSON files in the specified directory into one CSV with the specified
       outputfile name.  origdir specifies the directory prefix to the original input files
       and is used to provide the path to the original input file (rather than the TikaRunner's
       output file) in the CSV""" 
    fileList = __listFilesInDir(JSONout)
    outputfile = os.path.basename(os.path.normpath(origdir))
    outputfile = "TikaMetadata_Output_" + outputfile +".csv"
    
    # Work out all headings
    prop_headings = set([])
    for file in fileList:
        fname   = os.path.basename(file)
        
        
        metadata = {}
        try:
            fileObj = open("\\\\?\\"+file, 'r', encoding="cp1252")# load json
            metadata = json.load(fileObj, encoding="latin-1")
        except:
            pass
        #print (metadata.keys())
        prop_headings|=set(metadata.keys())
    # append all property headings to the HEADINGS list
    #print (prop_headings)
    
    HEADINGS.extend(list(prop_headings))
    
    
    # now create an output file
    writer = csv.DictWriter(open(outputfile, 'w', encoding = "utf8"), HEADINGS, extrasaction='ignore', lineterminator='\r')
    writer.writeheader()
    
    # now re-run through all the files again and fill out each row 
    for file in fileList:
        fname   = os.path.basename(file)
        metadata = {}
        try:
            # load json
            fileObj = open("\\\\?\\"+file, 'r', encoding="utf-8")
            metadata = json.load(fileObj)
        except:
            try:
                fileObj = open("\\\\?\\"+file, 'r', encoding="latin-1")
                metadata = json.load(fileObj)
            except Exception as e:
                print (file, e) 
                metadata['Read TikaRunner Output'] = False
                
        # delete any data from keys from the IGNORE list
        for k in IGNORE:
            if k in metadata:
                metadata[k] = "Data removed. See JSON output file"
        
        # add in the filename
        relpath     = os.path.dirname(os.path.relpath(file, JSONout))
        absOutPath  = os.path.join(origdir, relpath, fname)
        metadata['Filename']=absOutPath[:-5]    # removes the added ".txt" also
        
        # write output to file
        writer.writerow(metadata)
		
        
        fileObj.close()
		
arg1 = input("Enter filepath of directory to scan: ")
arg1 = arg1.strip('"')
	
	
if not os.path.exists(arg1):
	    print ("Please enter a filepath for location of the files you want to scan. e.g: C:\\Users\\example")
	    exit(0)
JSONout = os.path.basename(os.path.normpath(arg1))
JSONout = JSONout+" JSON OUTPUT"
if not os.path.exists(JSONout):
      os.makedirs(JSONout)
	  
JSONout = os.getcwd()+"\\"+JSONout

if __name__ == '__main__':
    print('Running Apache Tika')
    tikagrab(arg1)
    print ("Creating CSV")
    jsonclean(arg1)
    processdir(arg1)
    print ("CSV Created")
    print ("Clearing JSON Files")
    shutil.rmtree("\\\\?\\"+JSONout)
    print ("Script Completed")
