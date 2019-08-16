from .main import main
from .excel_report import JSONtoExcel

import os
from shutil import copyfile

def foldersOfFoldersOfFiles():
    #group files to folder
    # folder_paths = [r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/sendable', r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/sendable2', r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/sendable3']
    # destination = [r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/batch_2', r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/batch_3', r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/batch_4']

    folder_paths = [r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/200 Invoice Copies/Internal']
    destination = [r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/200_invoices']

    for i in range(len(folder_paths)):
        ArrangeFilesintoFolder(folder_paths[i], destination[i])

def ArrangeFilesintoFolder(folder, destination):
    print("calling the function")

    #get unique file name
    unique_list = []
    for file in os.listdir(folder):
        if file.split('_')[0] not in unique_list:
            unique_list.append(file.split('_')[0])
            print(file.split('_')[0])
        folder_name = file.split('.')[0]
    print("Number of files: ", len(unique_list))

    #create directories in destination for unique file names
    for file in unique_list:
        if not os.path.isdir(destination + '/' + file):
            os.mkdir(destination + '/' + file)

    #copy all files here to their respective names
    for file in os.listdir(folder):
        copyfile(folder + '/' + file, destination + '/' + file.split('_')[0] + '/' + file)

    print("toFolder: copying done")


def folderofdates():
    folder_path = r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/testingdocs_new'
    destination = r'C:/Users/JadaPrannoyNoelJada/Desktop/Ananth/testingdocs_new_output'

    for datefolder in [dI for dI in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path,dI))]:

        #arrange files in folder
        ArrangeFilesintoFolder2(folder_path + '/' + datefolder, destination)
        # break

def ArrangeFilesintoFolder2(folder, destination):
    # print("folder ", folder)
    # print("destination ", destination)
    for file in os.listdir(folder):
        # print("file: ", file)

        #check if file is a pdf
        if file.endswith('.pdf') or file.endswith('.PDF'):
            print(" In pdf")
            copyfile(folder + '/' + file, destination + '/' + file)
            continue

        #check if file is part of xml, text and tif group
        foldername = file.replace('c.', '.').split('.')[0]
        xml_path = os.path.join(folder, foldername + '.xml')
        tif_path = os.path.join(folder, foldername + '.tif')
        text_path = os.path.join(folder, foldername + '.txt')
        if os.path.exists(xml_path) and os.path.exists(tif_path) and os.path.exists(text_path):
            #folder in destination
            destination_folder = os.path.join(destination, foldername)
            if not os.path.isdir(destination_folder):
                os.mkdir(destination_folder)
            copyfile(os.path.join(folder, file), os.path.join(destination_folder, file))


if __name__ == '__main__':
    folder = os.path.join("C:\\", "Users", "JadaPrannoyNoelJada", "Documents", "Work", "Dow", "Results", "Set 2")
    source = os.path.join("C:\\", "Users", "JadaPrannoyNoelJada", "Documents", "Work", "Dow", "Results", "Set 2 source")
    destination = os.path.join("C:\\", "Users", "JadaPrannoyNoelJada", "Documents", "Work", "Dow", "Results", "Set 2 destination")

    #split files into folders
    ArrangeFilesintoFolder2(folder, source)

    #generate JSON from list of doc folders with OCR output and generate excel report in ./../report.xls
    for doc in [dI for dI in os.listdir(source) if os.path.isdir(os.path.join(source,dI))]:
        print("Doc ", doc)
        # for doc in os.listdir(folder_of_sources):
        try:
            doc_source = os.path.join(source, doc)
            doc_destination = os.path.join(destination, doc)
            # print(" ", doc_source)
            # print(" ", doc_destination)
            if os.path.exists(os.path.join(doc_destination, doc + '.json')):
                print(doc, " JSON generated")
            else:
                main(doc, 'yes', doc_source, doc_destination)
        except:
            print(doc, " failed")
        # break

    #excel generation
    excel_folder = destination
    print('\n**********Generating report*************')
    JSONtoExcel(excel_folder)
