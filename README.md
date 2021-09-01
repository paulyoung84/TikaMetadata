# TikaMetadata
Uses Apache Tika to run over a folder of files and generate a CSV output of metadata pulled from files

TikaMetadata Readme

About the script
This script uses Apache Tika to run over digital and grab additional metadata from within the format, creating a spreadsheet of the metadata for analysis.
The script requires you to download Apache Tika version tika-server-1.24.1.jar and tika-server-1.24.1.jar.md5 - https://repo1.maven.org/maven2/org/apache/tika/tika-server/ - and include within the clone folder, it also needs Java installed to run.

Running the script:

1.	Run TikaMetadata.bat

2.	It will open a window with a prompt to enter the filepath of the directory you want to scan. It should be run over a folder rather than single files. (You can drag the folder into the window for the path to populate the file path)

3.	The script will then run through the directory, it runs through each file seperately and prints on screen when it has completed scanning, or an error if it fails. It will output a CSV file as the final results in the same directory, it will have a column added called TikaRun which will state if that file was able to be scanned succesfully or not.

Notes:

This is still an early version of the script in test stages and you may see some formatting issues in the CSV output. Please let us know any issues you have and we can try to fix them for future versions.
