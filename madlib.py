import sys
import os

str_path_text="./texts"

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


def parse_raw_str(raw: str):
    """
    This function breaks down a single string into a list of strings that can be used as prompts.
    :param raw is one string that will be parsed into a list of strings that can be used as prompts :
    :return two lists of strings: one of inputs, one of the raw string minus the variable names :
    """
    list_variables = []
    list_raw = []
    str_temp = ""
    str_raw = ""
    bool_variable = False

    for i in raw:
        if i == "{":
            str_raw += "{"
            list_raw.append(str_raw)

            bool_variable = True
            str_temp = ""
            str_raw = ""
            continue

        elif i == "}":
            if str_temp != "":
                list_variables.append(str_temp)
                str_temp = ""

            str_raw = "}"
            bool_variable = False
            continue
        if bool_variable:
            str_temp += i
        else:
            str_raw += i

    list_raw.append(str_raw)

    return list_variables, list_raw


def prompts(list_par: list[str]) -> list[str]:
    '''
    Input a list of strings into this function. It will iterate over the list prompting the user for input that will be returned as a separate list of strings.
    :param list_par is a list of strings used to prompt the user:
    :return list of strings that the user has input:
    '''
    int_len = len(list_par)
    if int_len == 0:
        print("Test inside 'raw.txt' file isn't properly formated.")
        return []

    list_inputs = []
    count = 0

    while count < int_len:
        str_input = input(f'Enter a {list_par[count]}: ')
        if str_input==("quit"):
            bool_quit_game=True
            break
        list_inputs.append(str_input)
        count += 1

    return list_inputs


def format_str(str_par_raw: str, list_par_input: list[str]) -> str:
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

def make_list_of_files_available(str_path_par:str):
    list_text_files = sorted([i.split("_")[1] for i in os.listdir(str_path_par) if i.count("raw")])
    str_text_files = ", ".join([f'{value}({index + 1})' for index, value in enumerate(list_text_files)])
    return str_text_files, list_text_files


if __name__ == "__main__":
    print_message(str_madlib_description)

    #final all the file names that can be used as games
    str_text_files, list_text_files =make_list_of_files_available(str_path_text)

    #before jumping into the game
    str_enter_input =input("\n\nType any key and press enter to start: ")

    #the game lives in here and they can play as long as they don't type 'quit' into a prompt
    while not bool_quit_game:

        #print all script options for them to chose from
        print_message(f'\n\n{str_text_files}')
        str_path_input = input("\n\nChoose your adventure.\nHint, enter either number or name: ").lower()

        #parse user input into correct string to formate file path
        if str_path_input=="quit":
            bool_quit_game=True
            break
        elif str_text_files.count(str_path_input)>0:
            if list_text_files.count(str_path_input)>0:
                str_path_file=str_path_input
            else:
                str_path_file=list_text_files[int(str_path_input)-1]
        else:
            print_message("\n\nI didn't get that. Please try again.\n")
            continue

        #print script they have chosen
        print_message(f"\n\nYou chose '{str_path_file}'.")

        # open the raw file that will be used this round of the game
        with open(f'./texts/raw_{str_path_file}_game.txt', 'r') as raw:
            list_raw = "\n\n".join(raw.read().split("\n\n"))
            list_prompts, list_raw = parse_raw_str(list_raw)
            list_inputs = prompts(list_prompts)
            str_raw = "".join(list_raw)
            str_final = format_str(str_raw, list_inputs)
            print_message(f'\n\n{str_final}')

        #allow user to save results in file
        str_save_output=input("\n\nWould you like to save this script(y/n): ").lower()
        if str_save_output=="y":
            count=0
            while count<5:
                str_filename=input("\n\nWhat should we label the file.\n\nNames can only be a-z, A-Z, and 0-9 without spaces.\n\nAnd must be less than 20 characters long: ")
                if str_filename.isalnum() and len(str_filename)<21:
                    with open(f'./texts/fin_{str_filename}_game.text','w') as output:
                        output.write(str_final)
                        print_message(f'\n\n{str_filename}.txt successfully saved!')
                    count=5
                else:
                    count+=1
                    str_filename_continue=input("\n\nSorry that filename won't work.\n\nType any key to try again or 'cancel' to cancel saving file: ")
                    if str_filename_continue=='cancel':
                        count=5
        else:
            print_message("\n\nOkay, won't save this one.")

        #ask if they wish to keep playing
        str_keep_playing=input("\n\nWould you like to keep playing? Type any key to continue or 'quit' to stop: ")
        if str_keep_playing=="quit":
            bool_quit_game=True
            break

    #thank them for playing the game
    print_message(str_thank)
else:
    print("\n\nYou are not running the 'madlib_cli.py' script directly.\n")
