import os

from re_mover import clean_folder, move_stuff

def main():
    os.mkdir('public')
    clean_folder('public')
    move_stuff('static','public')

if __name__ == '__main__':
    main()