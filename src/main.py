import os
import sys

from main_helper import clean_folder, move_stuff, generate_pages_recursive

def main():
    root_path = sys.argv[1] if len(sys.argv)>1 else '/'
    output_path = sys.argv[2] if len(sys.argv)>2 else 'docs'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    clean_folder(output_path)
    move_stuff('static',output_path)
    
    content_path_abs = os.path.abspath('content/')
    dest_path_abs = os.path.abspath(output_path)      
    
    print(f"Generating pages from content/ to {output_path}/ using template.html")
    
    with open('template.html','r') as f:
        templet_cont = f.read()

    generate_pages_recursive(root_path,content_path_abs,templet_cont,dest_path_abs)
    #generate_pages_recursive('content/index.md','template.html','public/index.html')

if __name__ == '__main__':
    main()