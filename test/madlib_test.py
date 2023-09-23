import pytest
import os
from madlib import parse_raw_str, prompts, format_str, print_message, make_list_of_files_available

def test_read_template():
    with open('./texts/raw_short_game.txt') as short:
        list_short = "\n\n".join(short.read().split("\n\n"))
        list_prompts, list_short = parse_raw_str(list_short)
        str_short = "".join(list_short)
        str_expected="It was a {} and {} {}.\n"
        list_expected=["Adjective","Adjective","Noun"]
        assert str_short==str_expected, 'TEST FAILED, parse_raw_str() function not returning formated string.'
        assert all( [True if list_expected[index]==value else False for index,value in enumerate(list_prompts)]),"TEST FAILED, parse_raw_str() function not returning list of prompts."


def test_parse_template():
    str_short = "It was a {Adjective} and {Adjective} {Noun}.\n"
    list_short = "\n\n".join(str_short.split("\n\n"))
    list_prompts, list_short = parse_raw_str(list_short)
    str_short = "".join(list_short)
    str_expected = "It was a {} and {} {}.\n"
    list_expected = ["Adjective", "Adjective", "Noun"]
    assert str_short == str_expected, 'TEST FAILED, parse_raw_str() function not returning formated string.'
    assert all([True if list_expected[index] == value else False for index, value in
                enumerate(list_prompts)]), "TEST FAILED, parse_raw_str() function not returning list of prompts."

def test_merge_template():
    str_western = "Our {} hero {} into town on a {}. With only {} and {} on their mind."
    list_input = ["first",'second','third','fourth','fifth']
    str_formatted = format_str(str_western,list_input)
    str_expected = "Our first hero second into town on a third. With only fourth and fifth on their mind."
    assert str_formatted == str_expected,"TEST FAILED, format_str is not returning properly formated string"

# def test_prompts_template():
#     list_fake_prompts=['1','2','3']
#     list_input=prompts(list_fake_prompts)
#     int_expected=3
#     assert len(list_input)==int_expected,"TEST FAILED, prompts not returning same number of input strings as prompts provided"

def test_load_file_template():
    str_path='./texts/raw_fairytale_game.txt'
    try:
        with open(str_path,'r') as fairytale:
            pass
    except:
        assert False,'TEST FAILED, couldnt load file with given path'

def test_make_list_of_files_available_template():
    list_expected=sorted([i.split("_")[1] for i in os.listdir('./texts') if i.count('raw')>0])
    str_expected = ", ".join([f'{value}({index + 1})' for index, value in enumerate(list_expected)])
    str_files, list_files = make_list_of_files_available('./texts')
    assert all([True if list_expected[index]==value else False for index,value in enumerate(list_files)]), 'TEST FAILED, make_list_of_files_available() is not returning list of file names'
    assert str_expected==str_files,"TEST FAILED, make_list_of_files_available() is not returning properly formated string"
