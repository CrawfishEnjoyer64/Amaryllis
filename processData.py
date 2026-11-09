import xml.etree.ElementTree as etree
from gzip import GzipFile
import time
import os

#https://docs.python.org/3/library/concurrent.futures.html
import concurrent.futures #Recommended by a colleague.

def getelements(filename_or_file, tag):
    context = etree.iterparse(filename_or_file, events=("start", "end"))    # get iterator    
    _, root = next(context) # get the root element
    for event, elem in context:
        if event == 'end' and elem.tag == tag:
            yield elem
            root.clear() # free memory

searchedNation = "Your_Nation_Here"

def checkIfDownloaded(checkFor):
    return os.path.isfile(checkFor)

def report_from_file(filename_to_report):
    try:
        dynamic_spending_dictionary = {}
        dynamic_deaths_dictionary = {}

        path = filename_to_report.strip()

        with GzipFile(path) as dump_file: 
            for nation in getelements(dump_file, 'NATION'):
                #Check name
                name = nation.find(".//NAME").text
                public_spending_percentage = ""

                if(name == searchedNation):
                    government_spending = nation.find(".//GOVT")
                    for spending_category in list(government_spending):
                        if not (spending_category.tag in dynamic_spending_dictionary.keys()):
                            dynamic_spending_dictionary[spending_category.tag] = (spending_category.text)

                    death_causes = nation.find(".//DEATHS")
                    for cause_category in list(death_causes):
                        if not (cause_category.attrib['type'] in dynamic_deaths_dictionary.keys()):
                            dynamic_deaths_dictionary[cause_category.attrib['type']] = (cause_category.text)

                    public_spending_percentage = nation.find(".//PUBLICSECTOR").text

                    break

        information_string = filename_to_report[:10] + "*" + str(dynamic_spending_dictionary) + "*" + str(dynamic_deaths_dictionary) + "*" + str(public_spending_percentage)
    except:
        information_string = filename_to_report[:10] + "*" + "Failed."
    return information_string

def main():
    print("Program active... \n")

    #Load up all files as a tasklist to be completed
    list_of_files_to_process = []
    file_of_files = "set_of_files.txt" #Give this the files as needed on a one filename per line basis.

    with open(file_of_files) as requestFile:
        for file_name in requestFile:
            file_name_sanatized = file_name.strip()

            if(file_name_sanatized[-3:] == ".gz"):
                if(checkIfDownloaded(file_name_sanatized)):
                    list_of_files_to_process.append(file_name_sanatized)
                else:
                    print(file_name_sanatized + " was not found.")
            else:
                print(file_name_sanatized + " was not in the .gz format") #Some will show up as .bz2, and that is undesirable

    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.map(report_from_file,list_of_files_to_process)

    with open("output_data.txt", "a") as f:
        for row in list(result):
            f.write((row + "\n"))

    print("Program completed.\n")
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
