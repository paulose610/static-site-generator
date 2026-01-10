import os

from main_helper import clean_folder, move_stuff, generate_page

def main():
    if not os.path.exists('public'):
        os.mkdir('public')
    clean_folder('public')
    move_stuff('static','public')
    generate_page('content/index.md','template.html','public/index.html')

if __name__ == '__main__':
    main()