'''


AIJ Transcript Generator


'''

import os
import sys
import datetime
import SeleniumYT as syt

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
    

def getLinks(AIJ_data_filename="./AIJ_full_data.csv"):
    '''
    '''
    links = []
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
        #print(data)
        posted = data[1].split(' ')
        date = posted[0].split('/')

        try:
            video_date = datetime.datetime(int(date[2])+2000, int(date[0]),int(date[1]))

            if video_date < today:
                print("{} : Available".format(data[2]))
                links.append(data[3])
            else:
                print("{} : Not Available".format(data[2]))
        except Exception as e:
            print(e,data)
            continue
        
    return links

usage = '''
Usage: AIJ_transcript [AIJ_Full_data.csv] [Output Directory]

    AIJ_Full_data.csv - Full path to the csvv file containing
        the full coda data from the Active Inference Journal

    Output Directory - Full path to the output directory for
        the transcripts. The folder will be created if it
        doesn't already exists.

    This function takes a csv download of the coda full
    data and for each youtube link extracts the avaialble
    transcript from the youtube video.
'''

if __name__ == "__main__":

    argc = len(sys.argv)

    if argc < 2:
        print(usage)
    else:
        filename = sys.argv[1]
        links = getLinks(filename)

        if argc >= 3:
            out_dir = argv[2]
        else:
            out_dir = "./AIJ/"

        if len(links) > 0:
            # Start Service
            service = syt.startService()
            if service != None:
                # Open the Chrome driver
                for url in links:
                    try:
                        syt.getTranscription(service, url, True, out_dir)
                    except Exception as e:
                        print(e)
                        pass

                service.stop()
            else:
                print("Service crashed")

    

    
