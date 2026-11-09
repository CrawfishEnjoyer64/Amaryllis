import os.path
import urllib.request
import time


def checkIfDownloaded(checkFor):
    return os.path.isfile(checkFor)

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mechanocracy Archive Tool')]
urllib.request.install_opener(opener)

#Load a file containing what we *might* need to download
with open("toRequest.txt") as requestFile:
    for file_name in requestFile:
        if(file_name.strip()[-3:] == ".gz"):
            if(not checkIfDownloaded(file_name.strip())):
                print("Downloading: " + file_name.strip() + "...")

                #https://www.nationstates.net/archive/nations/2026-10-24-nations-xml.gz
                url_prefix = "https://www.nationstates.net/archive/nations/"
                url_to_retrieve = url_prefix + file_name.strip()
                urllib.request.urlretrieve(url_to_retrieve, file_name.strip())
                time.sleep(50) #This is a total guess as to what a reasonable value is. Use at own risk.
                print("File download complete.")

print("All downloads completed, have a nice day!")





