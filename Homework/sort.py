import os
from pathlib import Path
import shutil
import re


path_ = Path(r'/Users/marinavakulenko/Documents/Folder/to_sort')
allFilesList = list()


filters = { 
            'image'   : ['JPEG', 'PNG', 'JPG', 'SVG'],
            'video'   : ['AVI', 'MP4', 'MOV', 'MKV'],
            'document': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
            'music'   : ['MP3', 'OGG', 'WAV', 'AMR'],
            'archive' : ['ZIP', 'GZ', 'TAR']
        
            
          }

destFolders = {
                'image'    : r'/Users/marinavakulenko/Documents/Folder/sort/image',
                'video'    : r'/Users/marinavakulenko/Documents/Folder/sort/video',
                'document' : r'/Users/marinavakulenko/Documents/Folder/sort/document',
                'music'    : r'/Users/marinavakulenko/Documents/Folder/sort/music',
                'archive'  : r'/Users/marinavakulenko/Documents/Folder/sort/archive',
                'unknown'  : r'/Users/marinavakulenko/Documents/Folder/sort/unknown' 
             }

def get_ListOfFiles(dirName):
    listOfFiles = os.listdir(dirName)
    allFiles = list()

    for entry in listOfFiles:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_ListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

def createFolder(destFol):
    for df_k, df_v in destFolders.items():
        if not os.path.exists(df_v):
            os.makedirs(df_v, exist_ok=True)
            print(f"Folder created {df_v}")

    return True



def checkExtension(file_):
    for key_f, val_f in filters.items():
        for v in val_f:
            if file_.upper().find('.' + v) > 0:
                
                return key_f
            else:
                return "unknown"




music_files = []
def sortFile(files_):
    for f in files_:
        ext = ''
        ext = checkExtension(f)
        for type, destFolder in destFolders.items():
            if type == ext:
                # what to do with exisiting file - the same name
                destPath = destFolder + '/' + f.split('/')[-1] 

                print(f, destPath) # + r'\' + f.split())
                shutil.move(f, destPath)
            else:
                destPath = destFolders['unknown'] + '/' + f.split('/')[-1] 



listOfSortedFiles = []

def createListOfSortedFiles(desFold):
    for dk, dv in desFold.items():
        for a in get_ListOfFiles(dv):
            #print(a)
            listOfSortedFiles.append(a)
    

    return listOfSortedFiles




def getListOfExt():
    list_extensions = []
   
    for key_, val in destFolders.items():
        if key_ != "unknown":
            
            list_files = (get_ListOfFiles(val))
        
            for el in list_files:
                
                list_extensions.append(el.split("/")[-1].split(".")[-1])
                
    return list(set(list_extensions))
                



def getListUnknownExt():
   
    list_unknown_ext = []
    for key_, val in destFolders.items():
        if key_ == "unknown":
            list_files = (get_ListOfFiles(val))
        
            for el in list_files:
                
                list_unknown_ext.append(el.split("/")[-1].split(".")[-1])

               
    return list(set(list_unknown_ext))   


CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC, LATIN):
    
    TRANS[ord(c)] = l
    #TRANS.update({ord(CYRILLIC_SYMBOLS[i]):LATIN[i]})
    TRANS[ord(c.upper())] = l.upper()

    


def normalize(name: str)-> str:

    translated = name.translate(TRANS)
    translated = re.sub(r'\W','_', translated)
    return translated





def rename_files_in_folder(folder):

    result = get_ListOfFiles(folder)
    for path in result:

        file_path_source = path
        l = path.split("/")
        lista = l[-1].split(".")
        lista[0] = normalize(lista[0])
        l[-1] = ".".join(lista)
        file_path_dest = "/".join(l)
        os.rename(file_path_source, file_path_dest)
    
    return True




def rename_allFiles_inAll_folders():
    for k_dest,v_dest in destFolders.items():
        rename_files_in_folder(v_dest)
    return True 






createFolder(destFolders)
allFilesList = get_ListOfFiles(path_) 
sortFile(allFilesList)

for el in createListOfSortedFiles(destFolders):
    print(el)
print(getListUnknownExt())
print(getListOfExt())


rename_allFiles_inAll_folders()