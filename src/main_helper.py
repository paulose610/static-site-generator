import os
import shutil

from helper.md_to_html import markdown_to_html_node

def clean_folder(folder):
    #print('cleaning public folder')
    folder_path = os.path.abspath(folder)
    dirs = os.listdir(folder_path)
    for i in dirs:
        i_path = os.path.join(folder_path,i)
        if i!='__init__.py' and os.path.isfile(i_path):
            os.remove(i_path)
        elif os.path.isdir(i_path):
            clean_folder(f'{folder}/{i}')
            os.rmdir(os.path.abspath(f'{folder}/{i}'))


def move_stuff(here,there):
    #print('moving static content from static to public')
    folder_path = os.path.abspath(here)
    dest_path = os.path.abspath(there)
    dirs = os.listdir(folder_path)
    for i in dirs:
        i_path = os.path.join(folder_path,i)
        if i!='__init__.py' and os.path.isfile(i_path):
            shutil.copy(here+'/'+i,dest_path)
        elif os.path.isdir(i_path):
            new_dest_path = dest_path+'/'+i
            os.mkdir(new_dest_path)
            move_stuff(f'{here}/{i}',new_dest_path)


def extract_title(markdown):
    try:
        title = markdown.split('\n', 1)[0].split(' ')[1]
        return title
    except IndexError:
        raise ValueError("Title not found in the markdown.")
    

# def generate_page(from_path, template_path, dest_path):
#     md_cont = None
#     try:
#         with open(from_path,'r') as f:
#             md_cont = f.read()
#         with open(template_path,'r') as f:
#             template_cont = f.read()    
    
#     except Exception as e:
#         raise ValueError(e)
    
#     md_html = markdown_to_html_node(md_cont).to_html()
    
#     actual_title = extract_title(md_cont)

#     template_cont = template_cont.replace("{{ Title }}", actual_title)
#     template_cont = template_cont.replace("{{ Content }}", md_html)

#     with open(dest_path, 'w') as f:
#         f.write(template_cont)

def generate_page(root_path,from_path, template_cont, dest_path):
    md_cont = None
    print(f"Generating page from {from_path.split('/')[-2:]}")
    try:
        with open(from_path,'r') as f:
            md_cont = f.read()
    except Exception as e:
        raise ValueError(e)
    
    md_html = markdown_to_html_node(md_cont).to_html()
    
    actual_title = extract_title(md_cont)

    template_cont = template_cont.replace("{{ Title }}", actual_title)
    template_cont = template_cont.replace("{{ Content }}", md_html)
    template_cont = template_cont.replace("href='/", f"href='{root_path}")
    template_cont = template_cont.replace("src='/", f"src='{root_path}")

    with open(dest_path, 'w') as f:
        f.write(template_cont)

def generate_pages_recursive(root_path,content_dir_path, template_cont, dest_dir_path):
    dir_cont = os.listdir(content_dir_path)
    for i in dir_cont:
        i_path = os.path.join(content_dir_path,i)
        if os.path.isfile(i_path):
            des_path = os.path.join(dest_dir_path,i.split('.')[0]+'.html')
            generate_page(root_path,i_path,template_cont,des_path)
        elif os.path.isdir(i_path):
            des_path = os.path.join(dest_dir_path,i)
            os.mkdir(des_path)
            generate_pages_recursive(root_path,i_path,template_cont,des_path)