from pypdf  import PdfReader, PdfWriter
from os     import system, path, listdir, stat
from sys    import argv
import readline

from config import *

# set colors
red = '\033[38;2;225;0;0m'
green = '\033[38;2;0;220;0m'
blue = '\033[38;2;150;150;255m'
grey = '\033[38;2;150;150;150m'
reset = '\033[0m'

def print_metadata(new_metadata) -> None:
    global red, green, blue, grey, reset
    # get longest key length
    key_len = 0
    keys = []
    for key in new_metadata:
        key_len = max(key_len, len(key))
        keys.append(key)

    keys.sort()

    # print metadata
    filename_text = 'Filename'
    while len(filename_text) < key_len+5:
        filename_text += '.'
    print(filename_text + INPUTFILE + '\n')

    for key in keys:
        org_key = key
        while len(key) < key_len+5:
            key += '.'
        if new_metadata[org_key][1] == '[added]': print(green, end='')
        if new_metadata[org_key][1] == '[edited]': print(blue, end='')
        if new_metadata[org_key][1] == '[deleted]': print(red, end='')
        if org_key in ['/CreationDate', '/ModDate']:
            # convert date to a readable form
            value = new_metadata[org_key][0]
            date = f'   [{value[2:6]}-{value[6:8]}-{value[8:10]} {value[10:12]}:{value[12:14]}:{value[14:16]}]'
            print(reset+grey, end='')
            print(key + new_metadata[org_key][0] + date + reset)
        else:
            print(key + new_metadata[org_key][0] + reset)


def rlinput(prompt, prefill=''):
    # Editable input with readline module
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def main() -> None:
    global INPUTFILE, reader, writer, metadata, red, blue, reset

    new_metadata = reader.metadata.copy()

    for key in new_metadata:
        new_metadata[key] = [new_metadata[key], '']

    # loop
    while True:
        system('clear')
        
        print_metadata(new_metadata)

        # show menu
        print('\n---------- Menu ----------')
        print('\n ' + green + '[A]dd   ' + blue + '[E]dit   ' + red + '[D]elete' + reset)
        print('\n [Q]uit')
        choice = input('\n > ')

        # get input
        if choice != '':
            key = choice.lower().strip()[0]
        else:
            key = choice

        # do something
        system('clear')
        if key == 'q':
            metadata = new_metadata.copy()
            new_metadata = {}
            for key in metadata:
                if metadata[key][1] != '[deleted]':
                    new_metadata[key] = metadata[key][0]


            if new_metadata == reader.metadata:
                exit()

            if input('Save changes? (Y/n): ').lower().strip().startswith('n'):
                print(blue + '[INFO]: changes don\'t saved' + reset)
                exit()
            else:
                system('clear')
                if CREATE_BACKUPFILE:
                    print(blue + '[INFO]: Making backup...' + reset)
                    
                    system('cp "' + INPUTFILE + '" "' + INPUTFILE+'.original"')
                    
                    print(blue + '[INFO]: backup saved successfully' + reset)

                print(blue + '[INFO]: Saving file...' + reset)

                writer.add_metadata(new_metadata)

                # save metadata
                with open(INPUTFILE if OVERWRITE_INPUTFILE else 'output.py', "wb") as out_file:
                    writer.write(out_file)
                
                print(blue + '[INFO]: file saved successfully' + reset)
                exit()
            
        elif key == 'a':
            print_metadata(new_metadata)
            print('\n--------------------------')

            key   = input('\nMetadata Key  : ')

            if len(key.strip()) == 0:
                system('clear')
                input(red + '[ERROR]: You need to enter a metadata key' + reset)
            elif key in new_metadata and new_metadata[key][1] != '[deleted]':
                system('clear')
                input(red + '[ERROR]: key "' + key + '" already exists; use edit instead' + reset)
            else:
                if key[0] != '/':
                    key = '/' + key

                value = input('Metadata Value: ')
                if len(value.strip()) == 0:
                    system('clear')
                    input(red + '[ERROR]: You need to enter a metadata value' + reset)
                else:
                    # set metadata
                    new_metadata[key] = [value, '[added]']

        elif key == 'e':
            print_metadata(new_metadata)
            print('\n--------------------------')

            key   = input('\nMetadata Key  : ')

            if key[0] != '/':
                key = '/' + key

            count = 0
            for metakey in new_metadata:
                if metakey.startswith(key) and new_metadata[metakey][1] != '[deleted]':
                    new_key = metakey
                    count += 1
            if count > 1:
                system('clear')
                input(red + '[ERROR]: cannot identify key; key is not unique' + reset)
            elif count == 1:
                if key != new_key:
                    print(blue + '[INFO]: Successfully identified metadata key: ' + new_key + reset)
                key = new_key

                if len(key.strip()) == 0:
                    system('clear')
                    input(red + '[ERROR]: You need to enter a metadata key' + reset)
                elif key in ['/CreationDate', '/ModDate']:
                    system('clear')
                    input(red + '[ERROR]: You cannot edit this value' + reset)
                elif key in new_metadata and new_metadata[key][1] != '[deleted]':
                    value = rlinput('Metadata Value: ', new_metadata[key][0])
                    if len(value.strip()) == 0:
                        system('clear')
                        input(red + '[ERROR]: You need to enter a metadata value' + reset)
                    else:
                        # set metadata
                        new_metadata[key][0] = value
                        new_metadata[key][1] = '[edited]'
                else:
                    system('clear')
                    input(red + '[ERROR]: No key named '+key + reset)
            else:
                system('clear')
                input(red + '[ERROR]: No key named '+ key + reset)

        elif key == 'd':
            print_metadata(new_metadata)
            print('\n--------------------------')

            # get key to delete
            key = input('Metadata Key: ')

            if key[0] != '/':
                key = '/'+key
            
            count = 0
            for metakey in new_metadata:
                if metakey.startswith(key) and new_metadata[metakey][1] != '[deleted]':
                    new_key = metakey
                    count += 1
            if count > 1:
                system('clear')
                input(red + '[ERROR]: cannot identify key; key is not unique' + reset)
            elif count == 1:
                if key != new_key:
                    print(blue + '[INFO]: Successfully identified metadata key: ' + new_key + reset)
                key = new_key

                if key not in new_metadata.keys():
                    input(red + '[ERROR]: No key named '+ key + reset)
                elif key in ['/CreationDate', '/ModDate']:
                    system('clear')
                    input(red + '[ERROR]: You cannot delete this key' + reset)
                else:
                    # set metadata
                    new_metadata[key][1] = '[deleted]'
            else:
                system('clear')
                input(red + '[ERROR]: No key named '+ key + reset)


if __name__ == '__main__':
    inputfile = ''
    # chack if there are extra arguments
    if len(argv) < 2:
        print(red + '[ERROR]: You forget to set the input file!\n[ERROR]: Use "python3 ' + argv[0] + ' <filename.pdf>" instead!' + reset)
        exit()
    inputfile = argv[1]

    # check if first extra argument is a inputfile
    if inputfile != '':
        if not inputfile.endswith('.pdf'):
            print(red + '[ERROR]: input file needs to be a pdf' + reset)
            exit()
        else:
            INPUTFILE = inputfile
 
    if path.getsize(INPUTFILE) == 0:
        print(red + '[ERROR]: input file ' + INPUTFILE + ' is empty' + reset)
        exit()


    # create reader and writer
    reader = PdfReader(INPUTFILE)
    writer = PdfWriter()

    # get writer
    writer.append_pages_from_reader(reader)

    # start
    main()