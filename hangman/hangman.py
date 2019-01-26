import os
import sys
import random
import json
import re

# word directory
PATH = "word"


# collect all files name in specific path
def get_files_name(PATH):
    category_list = []
    for file in os.listdir(PATH):
        category_list.append(file.strip(".txt"))
    return category_list


# verify category input
# try/except will prevent exception if input is in wrong format
def is_wrong_category(selected_category, category_size):
    try:
        (int(selected_category))
    except:
        return True
    else:
        if(int(selected_category) <= category_size):
            return False
        else:
            return True


def prepare_data():
    category_list = get_files_name(PATH)
    print("Please select category \n")
    print_list_item_with_index(category_list)

    # let player select category in format number
    selected_category = input("\nyour category is : ")

    # this loop will not end until user enter category correctly
    while (is_wrong_category(selected_category, len(category_list))):
        print("please enter only number in length %d" % len(category_list))
        selected_category = input("\nyour category is : ")

    selected_category = category_list[(int(selected_category) - 1)]
    print("\nCategory : " + selected_category)
    word_list = get_word_from_txt(selected_category)
    return word_list


# get all word in text files
def get_word_from_txt(selected_category):
    # cd to path directory
    os.chdir(PATH)
    words_path = (selected_category + ".txt")
    # "r" stand for read only
    with open(words_path, "r") as file:
        # use json library convert txt file to dict (word:hint)
        # json need double quote so we must change it
        word_list = json.loads(file.read().replace("'", "\""))
        return word_list


# print all items in list with index
def print_list_item_with_index(category_list):
    # use enumerate in order to get index number
    for index, word in enumerate(category_list):
        print(index + 1, word)


def is_player_continuable(life, answer_unique_char, correct_guess_char):
    if(life == 0 or len(correct_guess_char) == len(answer_unique_char)):
        return False
    else:
        return True


# print character if player has guess correctly else print '_'
def print_remaining_char(current_word, correct_guess_char):
    for char in current_word:
        if (char.lower() in correct_guess_char or not char.isalpha()):
            print(char, end=' ')
        else:
            print("_", end=' ')


def remove_duplicate_char(string):
    return "".join(set(string.lower()))


word_list = prepare_data()

# randomize word to play
current_word = random.choice(list(word_list))
print("Hint: " + word_list[current_word])
# answer_unique_char is current word without duplicate char
# answer_unique_char is set of answer
answer_unique_char = remove_duplicate_char(current_word)
# remove non alphabet character
answer_unique_char = re.sub("[^a-zA-Z]+", "", answer_unique_char)

correct_guess_char = []
wrong_guess_char = []
life = 6
score = 0
# game start here
# this loop will end if player has guess all character correctly or life gone to zero
while(is_player_continuable(life, answer_unique_char, correct_guess_char)):
    print("\nyour life: %d, your score: %d" % (life, score))
    # print wrong guess character only when wrong_guess_char are not empty
    if (len(wrong_guess_char) > 0):
        print("your wrong guess: ", end='')
        [print(char, end=' ') for char in wrong_guess_char]
        print()

    print_remaining_char(current_word, correct_guess_char)
    player_guess_char = (input("\nEnter guess: "))
    # case-insensitive
    player_guess_char = player_guess_char.lower()
    # correct_guess_char should not collect duplicate character
    if (player_guess_char in answer_unique_char and player_guess_char not in correct_guess_char):
        correct_guess_char.append(player_guess_char)
        score += life
    # wrong_guess_char too
    elif (player_guess_char not in wrong_guess_char):
        wrong_guess_char.append(player_guess_char)
        life -= 1

# game end
if(life > 0):
    print("\nyou win!!!")
else:
    print("\nyou lose...")
print("your score: %d" % score)
print("Answer: " + current_word)

# prevent from closing immediately
input("\nPress enter to close program")
