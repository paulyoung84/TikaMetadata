import os
filepath = os.getcwd()
os.environ['TIKA_SERVER_JAR'] = 'file:////'+filepath+'\\tika-server-1.28.4.jar'
import tika
from tika import parser
import pandas as pd
import json
from pandas import json_normalize
import os.path
import hashlib


IGNORE = ['X-TIKA:content', 'X-TIKA:EXCEPTION:embedded_stream_exception','PCF1','Chroma Palette PaletteEntry','Blue Colorant','Blue TRC','Green Colorant','Green TRC','Red Colorant','Red TRC']

directory_to_scan = input("Enter filepath of directory to scan: ")
directory_to_scan = directory_to_scan.strip('"')
directory_to_scan = "\\\\?\\" + directory_to_scan

if not os.path.exists(directory_to_scan):
        print("Please enter a filepath for location of the files you want to scan. e.g: C:\\Users\\example")
        exit(0)

outputfile = os.path.basename(os.path.normpath(directory_to_scan))
outputfile = "TikaMetadata_Output_" + outputfile +".csv"

df = pd.DataFrame()
for dirpath, dirnames, filenames in os.walk(directory_to_scan):
    for filename in filenames:
        try:
            file_path = os.path.join(dirpath, filename)
            parsed = parser.from_file(file_path, requestOptions={'timeout': 300})
            data = json_normalize(parsed['metadata'])
            data['FilePath'] = file_path
            data['FileName'] = filename
            data['TikaRun'] = 'Success' 
            with open(file_path, 'rb') as afile:
                    sha256_object = hashlib.sha256()
                    block_size = 65536 * sha256_object.block_size
                    chunk = afile.read(block_size)
                    while chunk:
                        sha256_object.update(chunk)
                        chunk = afile.read(block_size)
                    gethash = sha256_object.hexdigest()
                    data['sha256_checksum'] = gethash
            for k in IGNORE:
                if k in data:
                    data[k] = "Data removed for presentation purposes"
            df = data.append(df)
            print(filename, 'scanned by Tika')
        except:
            data['FileName'] = filename
            data['FilePath'] = dirpath
            data['TikaRun'] = 'Failed'
            print(filename, 'NOT scanned by Tika (failed)')


cols_to_move = ['FileName', 'FilePath', 'TikaRun', 'sha256_checksum']
df = df[ cols_to_move + [ col for col in df.columns if col not in cols_to_move ] ]
df.to_csv(outputfile,index=False, encoding='utf-8')
print('Scanning completed')
