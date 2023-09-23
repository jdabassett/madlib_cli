import pytest
from madlib import parse_raw_str, prompts, format_str, print_message, make_list_of_files_available

list_video_prompts=['Adjective', 'Adjective', 'A First Name', 'Past Tense Verb', 'A First Name', 'Adjective', 'Adjective', 'Plural Noun', 'Large Animal', 'Small Animal', "A Girl's Name", 'Adjective', 'Plural Noun', 'Adjective', 'Plural Noun', 'Number 1-50', 'First Name', 'Number', 'Plural Noun', 'Number', 'Plural Noun']

list_video_inputs=['majestic','purple','Scott','colored','JB','laughing','tickled','arrows','gorilla','butterfly','Betty','silly','test','striped','jackets','44',"Wilson's",'3','leaves','4','swords']


def test_read_template():
    with open('./texts/raw_short_game.txt') as short:
        list_short = "\n\n".join(short.read().split("\n\n"))
        list_prompts, list_short = parse_raw_str(list_short)
        str_short = "".join(list_short)
        str_expected="It was a {} and {} {}.\n"
        list_expected=["Adjective","Adjective","Noun"]
        assert str_short==str_expected, 'TEST FAILED, parse_raw_str() function not returning formated string.'
        assert all( [True if list_expected[index]==value else False for index,value in enumerate(list_prompts)]),"TEST FAILED, parse_raw_str() function not returning list of prompts."
