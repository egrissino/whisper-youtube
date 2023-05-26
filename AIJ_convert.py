'''


AIJ Transcript Name Converter


'''

import os
import shutil
import SeleniumYT as syt
import AIJ_transcript as aijt

if __name__ == "__main__":

    argc = len(sys.argv)
    if argc > 1:
        out_dir = sys.argv[1]

    print("Running in directory: " + out_dir)

    links = aijt.getLinks()

    # Rename to video name
    filename = out_dir + syt.getFilenameFromURL(url)
    newFilename = out_dir + links[url][2] + ".txt"

    if os.path.exists(filename):
        shutil.copy(filename, newFilename)
