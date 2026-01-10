import os
import shutil

def clean_folder(folder):
    folder_path = os.path.abspath(folder)
    print(folder_path)
    dirs = os.listdir(folder_path)
    print(dirs)
    for i in dirs:
        i_path = os.path.join(folder_path,i)
        if i!='__init__.py' and os.path.isfile(i_path):
            os.remove(i_path)
        elif os.path.isdir(i_path):
            clean_folder(f'{folder}/{i}')
            os.rmdir(os.path.abspath(f'{folder}/{i}'))


def move_stuff(here,there):
    folder_path = os.path.abspath(here)
    dest_path = os.path.abspath(there)
    print(folder_path)
    dirs = os.listdir(folder_path)
    print(dirs)
    for i in dirs:
        i_path = os.path.join(folder_path,i)
        if i!='__init__.py' and os.path.isfile(i_path):
            shutil.copy(here+'/'+i,dest_path)
        elif os.path.isdir(i_path):
            new_dest_path = dest_path+'/'+i
            os.mkdir(new_dest_path)
            move_stuff(f'{here}/{i}',new_dest_path)