'''


AIJ Transcript Name Converter


'''

import os
import sys
import shutil
import SeleniumYT as syt
import AIJ_transcript as aijt

if __name__ == "__main__":
    
    argc = len(sys.argv)

    in_dir = './ytd/'
    if argc > 1:
        in_dir = sys.argv[1]

    print("Running in directory: " + in_dir)

    out_dir = "./AIJ/"
    syt.checkCreateDir(out_dir)

    syt.DEBUG = False
    links = aijt.getLinks()

    for url in links:
        # Rename to video name
        filename = in_dir + syt.getFilenameFromURL(url)
        newFilename = out_dir + links[url][2] + ".txt"

        if os.path.exists(filename):
            if not os.path.exists(newFilename):
                shutil.copy(filename, newFilename)
                print("Copied new file: " + newFilename)
                
