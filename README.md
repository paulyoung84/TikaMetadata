# TikaMetadata
Uses Apache Tika to run over a folder of files and generate a CSV output of metadata pulled from files

TikaMetadata Readme

About the script
This script uses Apache Tika to run over digital and grab additional metadata from within the format, creating a spreadsheet of the metadata for analysis.
The script requires you to download Apache Tika version tika-app-1.19 - https://archive.apache.org/dist/tika/ - and needs Java installed to run.
Running the script

1.	Run TikaMetadata.bat

2.	It will open a window with a prompt to enter the filepath of the directory you want to scan. It should be run over a folder rather than single files. (You can drag the folder into the window for the path to populate the file path)

3.	The script will then run through the directory, first of all creating a folder where you are running the script for the JSON output which Tika is creating. It then generates the DROID information. These two sets of information are then merged into a single CSV file, which is called TikaMetadata_Output_(name of folder run over).csv, the output will appear in the folder you ran the .py or .bat file.

Notes:

This is still an early version of the script in test stages and you may see some formatting issues in the CSV output. Please let us know any issues you have and we can try to fix them for future versions.
