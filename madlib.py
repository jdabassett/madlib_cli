import sys


# str_example="It was a {Adjective} and {Adjective} {Noun}."
# list_example_prompts=["Adjective","Adjective","Noun"]
# list_example_inputs=["cold","wet","day"]

def parse_raw_str(raw:str):
    """
    This function breaks down a single string into a list of strings that can be used as prompts.
    :param raw is one string that will be parsed into a list of strings that can be used as prompts :
    :return two lists of strings: one of inputs, one of the raw string minus the variable names :
    """
    list_variables=[]
    list_raw=[]
    str_temp=""
    str_raw=""
    bool_variable=False

    for i in raw:
        if i=="{":
            str_raw+="{"
            list_raw.append(str_raw)

            bool_variable=True
            str_temp=""
            str_raw = ""
            continue

        elif i=="}":
            if str_temp!="":
                list_variables.append(str_temp)
                str_temp=""

            str_raw="}"
            bool_variable=False
            continue
        if bool_variable:
            str_temp+=i
        else:
            str_raw+=i

    list_raw.append(str_raw)

    return list_variables, list_raw

def prompts(list_par:list[str])->list[str]:
    '''
    Input a list of strings into this function. It will iterate over the list prompting the user for input that will be returned as a separate list of strings.
    :param list_par is a list of strings used to prompt the user:
    :return list of strings that the user has input:
    '''
    int_len=len(list_par)
    if int_len==0:
        print("Test inside 'raw.txt' file isn't properly formated.")
        return []

    list_inputs=[]
    count=0

    while count<int_len:
        str_input = input(f'Enter a {list_par[count]}: ')
        list_inputs.append(str_input)
        count+=1

    return list_inputs

def format_str(str_par_raw:str,list_par_input:list[str])->str:
    return str_par_raw.format(*list_par_input)


if __name__=="__main__":
    dict_argv={index:value for index,value in enumerate(sys.argv)}
    if 1 not in dict_argv and dict_argv[1].find("raw")!=-1:
        print("Must provide raw text file to be imported and parsed. ie...'python madlib.py texts/raw_short_game.txt'")
    else:
        # open the raw file that will be used this round of the game
        with open(f'./{dict_argv[1]}', 'r') as raw:
            list_raw = "\n".join(raw.read().split("\n\n"))

            list_prompts, list_raw = parse_raw_str(list_raw)

            list_inputs = prompts(list_prompts)

            str_raw = "".join(list_raw)

            # print(list_prompts)
            # print(list_inputs)
            # print(list_raw)
            # print(str_raw)

            print(format_str(str_raw, list_inputs))



else:
    print("You are not running the 'madlib_cli.py' script directly.")
