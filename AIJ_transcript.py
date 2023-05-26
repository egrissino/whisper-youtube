'''


AIJ Transcript Generator


'''

import os
import sys
import datetime
import SeleniumYT as syt
from shutil import move

def splitLine(line, sep=','):
    data = []
    inQuote = False

    elem = ""
    for char in line:
        if char == '"':
            inQuote = not inQuote

        if (char == sep) and not inQuote:
            data.append(elem)
            elem = ""
        else:
            elem += char

    return data


def sliceAtInd(array, count=-1):
    '''
    Slice array at index
    '''
    if count >= len(array):
        count = len(array)-1
    out = array[:count]
    out.append(array[count])
    return out

def moveFile(file, newFile):
    '''
    '''

def getLinks(AIJ_data_filename="./AIJ_full_data.csv"):
    '''
    '''
    links = {}
    # date in yyyy/mm/dd format
    today = datetime.datetime.now()

    #AIJ_data_filename = "/Users/evan/Documents/AIJ_full_data.csv"
    offset = 3

    if not os.path.exists(AIJ_data_filename):
        print("File not Found! " + AIJ_data_filename)
        return
        
    infile = open(AIJ_data_filename, 'r', encoding='latin-1')
    inbuff = infile.readlines()
    infile.close()

    for line in inbuff[offset:]:
        data = splitLine(line) #line.split(',')
        posted = data[1].split(' ')
        date = posted[0].split('/')

        try:
            video_date = datetime.datetime(int(date[2])+2000, int(date[0]),int(date[1]))

            if video_date < today:
                syt.printDebug("{} : Available".format(data[2]))
                links[data[3]] = data
            else:
                syt.printDebug("{} : Not Available".format(data[2]))
        except Exception as e:
            syt.printDebug(e,data)
            continue
        
    return links

usage = '''
Usage: AIJ_transcript [AIJ_Full_data.csv] [Output Directory] [count]

    AIJ_Full_data.csv - Full path to the csvv file containing
        the full coda data from the Active Inference Journal

    Output Directory - Full path to the output directory for
        the transcripts. The folder will be created if it
        doesn't already exists.

    (optoinal) count - Total number of links to transcribe.

    (optional) Overwrite - T/F weather or not overwrite
        existing transcriptions.

    This function takes a csv download of the coda full
    data and for each youtube link extracts the avaialble
    transcript from the youtube video.
'''


if __name__ == "__main__":

    argc = len(sys.argv)
    #print(sys.argv)

    if argc < 2:
        print(usage)
    else:
        filename = sys.argv[1]

        out_dir = "./AIJ/"
        if argc >= 3:
            out_dir = sys.argv[2]

        count = -1
        if argc >= 4:
            try:
                count = int(sys.argv[3])
            except:
                pass

        overw = False
        if argc >= 5:
            for t in ["t","T","true","True","TRUE"]:
                if t in sys.argv[4]:
                    overw = True

        skips = []
        if argc >= 6:
            if os.path.exists(sys.argv[5]):
                skips = os.listdir(sys.argv[5])
                print(skips)
        
        links = getLinks(filename)

        
        if len(links) > 0:
            # Start Service
            service = syt.startService()
            if service != None:
                # Open the Chrome driver
                for url in sliceAtInd(list(links.keys()),count-1):
                    if ((links[url][2] + '.txt') in skips) and (not overw):
                        print("Skipping transcript: " + links[url][2])
                        continue
                    try:
                        syt.getTranscription(service, url, overw, out_dir)
                    except Exception as e:
                        print(e)
                        pass
                service.stop()
                print("Service stopped")
            else:
                print("Service crashed")

    

    
