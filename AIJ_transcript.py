'''


AIJ Transcript Generator


'''

import os
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
    

def getLinks():
    '''
    '''
    links = []
    # date in yyyy/mm/dd format
    today = datetime.datetime.now()


    AIJ_data_filename = "/Users/evan/Documents/AIJ_full_data.csv"
    offset = 3

    if not os.path.exists(AIJ_data_filename):
        print("File not Found!")
        quit()
        
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
                break
            else:
                print("{} : Not Available".format(data[2]))
        except Exception as e:
            print(e,data)
            continue
        
    return links


if __name__ == "__main__":

    links = getLinks()

    out_dir = "/Users/evan/AIJ"

    # Start Service
    service = syt.startService()
    if service != None:
        # Open the Chrome driver
        for url in links:
            syt.getTranscription(service, url)

    

    
