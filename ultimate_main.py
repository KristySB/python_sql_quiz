import pyodbc
import random
import os
from ultimate_handler import Handler
from ultimate_info import Info

ms_handler = Handler(server='DESKTOP-KH9HCHB\SQLEXPRESS', database='test_database', username='DESKTOP-KH9HCHB\notit') # type in your server and username
info_system = Info(ms_handler)

def print_menu():
    print('''
          -----------------------------------
         |    Welcome to the MS SQL QUIZ!    |
         |-----------------------------------|
         |  [PRESS 1] to start the quiz      |
         |  [PRESS 2] to insert a new player |
         |  [PRESS 3] to list the players    |
         |  [PRESS 0] to terminate           |
          -----------------------------------
          ''')
    
def list_players():
    os.system('cls')
    players = info_system.get_players()
    winner = []
    winner_points = 0
    all_winners = []

    if len(players) > 0:
        for one_player in players:
            print(f'{one_player[0]}. {one_player[1]} {one_player[2]} - {one_player[3]} points')
            if one_player[3] >= winner_points and one_player[3] != 0:
                winner.append(one_player)
                winner_points = one_player[3]
    
        if len(winner) >= 1:
            print('\n', end='')
            if len(winner) == 1:
                print(f'The best player is {winner[0][1]} {winner[0][2]} with {winner[0][3]} points')
            elif len(winner) > 1:
                print('The best players are:')
                for one_winner in winner:
                    print(f'{one_winner[1]} {one_winner[2]} with {one_winner[3]} points')

    else:
        print('No players')

def insert_player():
    os.system('cls')
    name = input('Name: ')
    surname = input('Surname: ')
    player_data = {'name': name, 'surname': surname, 'points': 0, 'answered_questions': 0}
    info_system.insert_player(player_data)
    print(f'''
                 -----------------------
                    Welcome, {name}!
                 -----------------------
          ''')
    
def quiz_repetition(player_number):
    print("\nHere are the questions you have answered incorrectly:\n")
    question_list = info_system.get_questions_repetition(player_number)

    for x in question_list:
        question = info_system.get_one_wrong_question(x)
        print(f'Question: {question[0][1]}\nAnswer: {question[0][2]}')
        print('\n')

def quiz(player_number, questions, all_questions):
    clue = 0

    # STARTING GAME
    while True:
        # QUESTION CHOOSING
        question = info_system.get_random_question()
        while str(question[0]) in questions:
            question = info_system.get_random_question()
        print(question[1])

        # PLAYER ANSWERING
        answer = input('Type the sql command. For clue print "0":\n')

        # CLUE
        if answer == '0':
            if clue < 3:
                clue += 1
                print(question[3])
            else:
                print('Sorry you have exhausted all clues for now.')
            answer = input('Type the sql command:\n')

        # CHECKING ANSWER
        os.system('cls')
        result = info_system.answer_execute(answer)
        right_answer = info_system.answer_execute(question[2])

        if result == right_answer:
            info_system.add_points(1, player_number)
            info_system.insert_answers(player_number, question[0], 'Y')
            score = info_system.get_points(player_number)
            print(f'Right answer! You have {score} points.')
        else:
            info_system.insert_answers(player_number, question[0], 'N')
            score = info_system.get_points(player_number)
            print(f'Wrong answer. The right answer was:\n{question[2]}\nYou have {score} poins.')
        
        # UPDATING DATA
        info_system.add_answered_question(player_number)
        questions = info_system.get_questions_by_player(player_number)
        player_questions = info_system.answered_questions_count(player_number)

        # CONTINUE YES OR NO
        score = info_system.get_points(player_number)

        if player_questions >= len(all_questions):
            print(f'You have finished the quiz. Your total score is {score}.')
            break
        else:
            cont = input('Do you want to continue? Respond "Y" or "N": ')
            while cont.upper() != 'Y' and cont.upper() != 'N':
                print('Sorry I did not understand.')
                cont = input('Do you want to continue? Respond "Y" or "N": ')
                os.system('cls')
            if cont.upper() == 'N':
                os.system('cls')
                print(f'You have finished the quiz for now. Your score is {score}.')
                break
            elif cont.upper() == 'Y':
                os.system('cls')
                continue

def game():
    os.system('cls')
    list_players()
    print('\n')
    player_number = int(input('Choose the player: '))
    os.system('cls')

    all_questions = info_system.get_all_questions()
    questions = info_system.get_questions_by_player(player_number) # finding all questions answered by the player
    player_questions = info_system.answered_questions_count(player_number)

    if len(all_questions) > player_questions:
        print("Let's start!\n")
        quiz(player_number, questions, all_questions)

    else:
        print('You have answered all of the questions.\n')
        user = input('''To restart all the quiz print "1".\n
To go over your wrong answered questions print "2": ''')
        answer_list = ['1', '2']

        while user not in answer_list:
            print('Sorry I did not understand.')
            user = input('''To restart all the quiz print "1".\n
To go over your wrong answered questions print "2": ''')
            
        if user == '1':
            info_system.drop_answers_by_player(player_number)
            os.system('cls')
            print("Let's start the quiz again!")
            questions = info_system.get_questions_by_player(player_number)
            quiz(player_number, questions, all_questions)

        elif user == '2':
            os.system('cls')
            quiz_repetition(player_number)

# GAME
while True:
    print_menu()
    user = input('Your choice: ')
    choice_list = ['1', '2', '3', '0']
    while user not in choice_list:
        print('Sorry I did not understand.')
        user = input('Your choice: ')
    if user == '1':
        game()
    elif user == '2':
        insert_player()
    elif user == '3':
        list_players()
    elif user == '0':
        print('Bye!')
        break