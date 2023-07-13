import os
from pathlib import Path
import shutil
import re

while True:

    user_folder = Path(input(r'Input directory: '))
    
    if user_folder.is_dir():
        break
    else:
        print("Your input is not a correct directory. Try again.")
        



allFilesList = list()

filters = { 
            'image'   : ['JPEG', 'PNG', 'JPG', 'SVG'],
            'video'   : ['AVI', 'MP4', 'MOV', 'MKV'],
            'document': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
            'music'   : ['MP3', 'OGG', 'WAV', 'AMR'],
            'archive' : ['ZIP', 'GZ', 'TAR']
        
            
          }

dest_folders = {
                'image'    : str(user_folder) + '/sort/image/',
                'video'    : str(user_folder) + '/sort/video/',
                'docs' : str(user_folder) + '/sort/docs/',
                'music'    : str(user_folder) + '/sort/music/',
                'archive'  : str(user_folder) + '/sort/archive/',
                'unknown'  : str(user_folder) + '/sort/unknown/'
             }

def get_list_of_files(dir_name):
    list_of_files = os.listdir(dir_name)
    allFiles = list()

    for entry in list_of_files:
        fullPath = os.path.join(dir_name, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

def create_folder(destFol):
    for df_k, df_v in dest_folders.items():
        if not os.path.exists(df_v):
            os.makedirs(df_v, exist_ok=True)
            print(f"Folder created {df_v}")

    return True



def check_extension(file_):
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
        ext = check_extension(f)
        for type, dest_folder in dest_folders.items():
            if type == ext:
                # what to do with exisiting file - the same name
                dest_path = dest_folder + '/' + f.split('/')[-1] 

                print(f, dest_path) # + r'\' + f.split())
                shutil.move(f, dest_path)
            else:
                dest_path = dest_folders['unknown'] + '/' + f.split('/')[-1] 



list_of_sorted_files = []

def create_list_of_sorted_files(dest_fold):
    for dk, dv in dest_fold.items():
        for a in get_list_of_files(dv):
            #print(a)
            list_of_sorted_files.append(a)
    

    return list_of_sorted_files




def get_list_of_ext():
    list_extensions = []
   
    for key_, val in dest_folders.items():
        if key_ != "unknown":
            
            list_files = (get_list_of_files(val))
        
            for el in list_files:
                
                list_extensions.append(el.split("/")[-1].split(".")[-1])
                
    return list(set(list_extensions))
                



def get_list_unknown_ext():
   
    list_unknown_ext = []
    for key_, val in dest_folders.items():
        if key_ == "unknown":
            list_files = (get_list_of_files(val))
        
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

    result = get_list_of_files(folder)
    
    for path in result:

        file_path_source = path
        l = path.split("/")
        lista = l[-1].split(".")
        lista[0] = normalize(lista[0])
        l[-1] = ".".join(lista)
        file_path_dest = "/".join(l)
        os.rename(file_path_source, file_path_dest)
    
    return True




def rename_all_files_in_all_folders():
    for k_dest,v_dest in dest_folders.items():
        rename_files_in_folder(v_dest)
    return True 




def run():
    
    create_folder(dest_folders)
    allFilesList = get_list_of_files(user_folder) 
    sortFile(allFilesList)
    for el in create_list_of_sorted_files(dest_folders):
        print(el)
    print(get_list_unknown_ext())
    print(get_list_of_ext())
    rename_all_files_in_all_folders()
    return True
    

if __name__ == "__main__":
    run()
