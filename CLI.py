#imports python
import csv
# Reaad File , write file
import os
import os.path
# getpwid used for getting file 's user name
import subprocess
import csv
import sys


metadata = []
fieldnames = []
dictapp = {}

#location of the exiftool
exifttoolpath = './exiftool/'

def file(path,csvfilename):
    fieldnames = ['File Name','Directory','File Size','File Type','Create Date','Modify Date','Encoder Settings',"Software",'Aperture Value','Brightness Value','Pixels Per Unit X','Pixels Per Unit Y','Pixel Units','Flash','Image Width','Image Height','Bit Depth','Color Type'
    ,'Compression',"F Number",'ISO','GPS Time Stamp','Aperture','Audio Sample Rate','Movie Data Size','Movie Data Offset','Handler Vendor ID','Audio Bits Per Sample','Image Size','App Version','Creator'
    ,'Doc Security','Hyperlinks' ,'Changed','LastSaved','Links Up To Date','Scale Crop','Artist','Album','Year','Video Frame Rate','Duration','MPEG Audio Version','Audio Layer','Audio Bitrate','Sample Rate','Channel Mode','MS Stereo','Genre','Copyright Flag'
    ,'Title','ID3 Size','PDF Version','Linearized','Page Count','Producer','Compatible Brands','Movie Header Version','Time Scale'
    ,'Duration','Preferred Rate','Preferred Volume','Preview Time','Preview Duration',"Poster Time","Camera Model Name"
    ,"Make","Resolution Unit",'Megapixels','Filter','Interlace','Significant Bits','Language','Revision Number','Subject','Template','Total Edit Time']

# its used for file open and create out.csv
    with open(csvfilename, 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        print("In Process")
        for entry in os.listdir(path):
            #if get directory then
            if os.path.isdir(os.path.join(path, entry)):
                #scan directory from given directory
                with os.scandir(os.path.join(path, entry)) as entries:
                    for ent in entries:
                        #if file then
                        if ent.is_file():
                            # take containt of file property
                            info = ent.stat()
                            #take file name
                            fileext = ent.name.split('.')[-1]
                            #file path
                            pathoffile = f'{path}/{entry}/{ent.name}'
                            d = extractmetadata(pathoffile)
                            if d:
                                for i in d:
                                    # print(d[i])
                                    try:
                                        writer.writerow(d)
                                    except:
                                        # print(e)
                                        pass
                
            else:
                if os.path.isfile(f'{path}/{entry}'):
                    info = os.stat(f'{path}/{entry}')
                    fileext = entry.split('.')[-1]
                    pathoffile = f'{path}/{entry}'
                    d = extractmetadata(pathoffile)
                    dictonary={}
                    if d : 
                        for i in d:
                            if i in fieldnames:
                                dictonary[i]=d[i]
                        writer.writerow(dictonary)
        csvFile.close()
        print("Success")
        print(csvfilename + " file saved successfully.")


# extract matadat 
def extractmetadata(filepath):

    try:
        # exe = 'hachoir-metadata'
        exe = '{}{}'.format(exifttoolpath, 'exiftool')
        process = subprocess.Popen(
            [exe, filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        info = {}
        for output in process.stdout:
            line = output.strip().split(':')
            # print(line[0])
            fieldnames.append(line[0].strip())
            info[line[0].strip()] = line[1].strip()
        return info
    except:
        print("Error occured")

# take input from user
print("\n--------------------------------------")
print("--------------------------------------")
print("-----  FILE META DATA HARVESTER  -----")
print("--------------------------------------")
print("--------------------------------------\n")
filepath=""
csvfile=""
for i in range(len(sys.argv)):
    if i < len(sys.argv) -1 and sys.argv[i] == '-r' and sys.argv[i+1] and sys.argv[i+1] != '-o':
        filepath= sys.argv[i+1]
    elif i < len(sys.argv) -1 and sys.argv[i] == '-o' and sys.argv[i+1] and sys.argv[i+1] != '-r':
        csvfile=sys.argv[i+1]
if( not filepath):   
    filepath = input("Please enter a directory/file to harvest: \n")
    
if( not csvfile):
    csvfile='out.csv'
try:
    # call file funcation with argument as filepath
    file(filepath,csvfile)
except FileNotFoundError as filenotfound:
    print("No such file or directory:", filepath)

