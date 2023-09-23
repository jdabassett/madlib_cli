import sys
import os

str_path_text="./assets"

bool_quit_game=False

str_madlib_description = """Hello, this is a game of MadLib!\n
Don't worry if you have never played before.\n
I will teach how to play.\n
Before I do, know that you can type 'quit' with any prompt to leave the game at anytime.\n
First you will chose from a list of scripts.\n
I will ask you for words to use with that script. Something like...'Enter a noun: '\n
I will then use your input to construct a new script we can share with everyone.\n
You can chose to save the script for posterity.
    """
str_thank="Thank you for playing my game. Come play again soon!"

def read_template(str_path:str)->str:
    with open(str_path,'r') as file:
        return file.read().strip()


def parse_template(str_raw: str):
    """
    This function breaks down a single string into a list of strings that can be used as prompts.
    :param raw is one string that will be parsed into a list of strings that can be used as prompts :
    :return two lists of strings: one of inputs, one of the raw string minus the variable names :
    """
    list_variables = []
    list_raw = []
    str_temp = ""
    str_sent = ""
    bool_variable = False

    for i in str_raw:
        if i == "{":
            str_sent += "{"
            list_raw.append(str_sent)

            bool_variable = True
            str_temp = ""
            str_sent = ""
            continue

        elif i == "}":
            if str_temp != "":
                list_variables.append(str_temp)
                str_temp = ""

            str_sent = "}"
            bool_variable = False
            continue
        if bool_variable:
            str_temp += i
        else:
            str_sent += i

    list_raw.append(str_sent)
    str_raw_return="".join(list_raw)

    return str_raw_return, list_variables


def prompts(list_par: list[str]):
    '''
    Input a list of strings into this function. It will iterate over the list prompting the user for input that will be returned as a separate list of strings.
    :param list_par is a list of strings used to prompt the user and boolean of whether to continue game:
    :return list of strings that the user has input and boolean of whether to continue game:
    '''
    int_len = len(list_par)
    if int_len == 0:
        print("\nTest inside 'raw.txt' file isn't properly formatted.")
        return [], False

    list_inputs = []
    count = 0

    while count < int_len:
        str_input = input(f'\nEnter {list_par[count]}: ')
        if str_input=="quit":
            return [], True
        list_inputs.append(str_input)
        count += 1

    return list_inputs, False


def merge(str_par_raw: str, list_par_input: list[str]) -> str:
    """
    :param str_par_raw is the raw string without the user inputs:
    :param list_par_input is a list of user inputs:
    :return formated string combining raw and input:
    """
    return str_par_raw.format(*list_par_input)


def print_message(str_par: str):
    """
    :param str_par to be printed in function:
    :return none:
    """
    print(str_par)

def format_filename(str_filename:str)->str:
    """
    takes in filename and returns formatted name of file, minus underscores, template, and file type
    :param str_filename is full filename:
    :return name of file as string:
    """
    int_index=str_filename.find("_template")
    str_return=str_filename[0:int_index]
    str_return=str_return.replace("_"," ")
    return str_return

def make_list_of_files_available(str_path_par:str):
    """
    searches directory for all filenames that contain '_template', returns string of concatenated file names and list of filenames
    :param str_path_par is a string path of directory to search:
    :return str_test_files is a concatenated string of file names, list_text_files is list of formatted filenames:
    """
    list_text_files = sorted([format_filename(i) for i in os.listdir(str_path_par) if i.count("_template")])
    str_text_files = "\n".join([f'({index + 1}) {value}' for index, value in enumerate(list_text_files)])
    return str_text_files, list_text_files

def save_script(str_final:str):
    # allow user to save results in file
    str_save_output = input("\nWould you like to save this script(y/n): ").lower()
    if str_save_output == "y":
        count = 0
        while count < 5:
            str_filename = input(
                "\nWhat should we label the file.\nNames can only be a-z, A-Z, and 0-9 without spaces.\nAnd must be less than 20 characters long: ")
            if str_filename.isalnum() and len(str_filename) < 21:
                with open(f'./assets/fin_{str_filename}.text', 'w') as output:
                    output.write(str_final)
                    print_message(f'\nfin_{str_filename}.txt successfully saved!')
                count = 5
            else:
                count += 1
                str_filename_continue = input(
                    "\nSorry that filename won't work.\nType any key to try again or 'cancel' to cancel saving file: ")
                if str_filename_continue == 'cancel':
                    count = 5
    else:
        print_message("\nOkay, won't save this one.")

def keep_playing()->bool:
    # ask if they wish to keep playing
    str_keep_playing = input("\nWould you like to keep playing? Type any key to continue or 'quit' to stop: ")
    if str_keep_playing == "quit":
        return True
    else:
        return False

def main(str_text_files:str,list_text_files:list[str]):
    """
    the brains of the game live here
    :param str_text_files:
    :param list_text_files:
    :return:
    """
    #the game lives in here and they can play as long as they don't type 'quit' into a prompt
    while True:

        #print all script options for them to chose from
        print_message(f'\n{str_text_files}')
        str_path_input = input("\nChoose your adventure.\nHint, enter either number or name: ").lower()

        #parse user input into correct string to formate file path
        if str_path_input=="quit":
            print_message(str_thank)
            break
        elif str_text_files.count(str_path_input)>0:
            if list_text_files.count(str_path_input)>0:
                str_path_file=str_path_input
            else:
                str_path_file=list_text_files[int(str_path_input)-1]
        else:
            print_message("\nI didn't get that. Please try again.\n")
            continue

        #print script they have chosen
        print_message(f"\nYou chose '{str_path_file}'.")

        # open the raw file that will be used this round of the game
        with open(f'./assets/{str_path_file.replace(" ","_")}_template.txt', 'r') as raw:
            str_raw, list_prompts = parse_template(raw.read())
            list_inputs, bool_prompts_quit = prompts(list_prompts)
            #quit game if false
            if bool_prompts_quit:
                break
            else:
                str_final = merge(str_raw, list_inputs)
                print_message(f'\n\nHere is your story: {str_final}')

        save_script(str_final)

        bool_end_quit=keep_playing()
        if bool_end_quit:
            break


if __name__ == "__main__":
    print_message(str_madlib_description)

    #final all the file names that can be used as games
    str_text_files, list_text_files =make_list_of_files_available(str_path_text)

    #before jumping into the game
    str_enter_input =input("\nType any key and press enter to start: ")
    # quit game if false
    if str_enter_input=="quit":
            bool_quit_game=True

    #brains of the game live here
    main(str_text_files,list_text_files)

    #thank them for playing the game
    print_message(str_thank)
else:
    print("\nYou are not running the 'madlib_cli.py' script directly.\n")
