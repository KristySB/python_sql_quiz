from ultimate_handler import Handler
import pyodbc

class Info:
    def __init__(self, db_handler: Handler):
        self.db_handler = db_handler

    def get_all_questions(self):
        all_questions = self.db_handler.get_data('test.sql_test', ['*'])
        return all_questions
    
    def get_random_question(self):
        question = self.db_handler.get_random_data('test.sql_test', ['*'])
        return question
    
    def insert_player(self, data_dict = {}):
        self.db_handler.insert_data('test.player', data_dict)

    def get_players(self):
        all_players = self.db_handler.get_data('test.player', ['*'])
        return all_players
    
    def get_points(self, player_id):
        previous_points = self.db_handler.get_data_conditioned('test.player', 'player_id', player_id, ['points'])
        previous_points = str(previous_points[0])
        signs = ['(', ',', ')']
        n = 0
        for x in range(0, len(signs)):
            previous_points = previous_points.replace(signs[n], '')
            n += 1
        return previous_points
    
    def add_points(self, points, player_id):
        self.db_handler.update_data_addition('test.player', 'points', points, 'player_id', player_id)

    def add_answered_question(self, player_id):
        self.db_handler.update_data_addition('test.player', 'answered_questions', 1, 'player_id', player_id)

    def insert_answers(self, player_id, quest_id, answer):
        self.db_handler.insert_data('test.answer', {'player_id': player_id, 'quest_id': quest_id, 'answer': answer})

    def get_questions_by_player(self, player_id):
        questions = self.db_handler.get_data_conditioned('test.answer', 'player_id', player_id, ['quest_id'])
        used_questions = []
        for x in questions:
            used_questions.append(str(x))

        signs = ['(', ',', ')']
        n = 0
        n1 = 0
        repeating = 0
        while repeating < len(signs):
            for x in used_questions:
                used_questions[n] = x.replace(signs[n1], '')
                n += 1
            n = 0
            n1 += 1
            repeating += 1
        return used_questions
    
    def answered_questions_count(self, player_id):
        number = self.db_handler.get_data_conditioned('test.player', 'player_id', player_id, ['answered_questions'])
        number = str(number[0])
        signs = ['(', ',', ')']
        n = 0
        for x in range(0, len(signs)):
            number = number.replace(signs[n], '')
            n += 1
        number = int(number)
        return number
    
    def drop_answers_by_player(self, player_id):
        self.db_handler.drop_data('test.answer', 'player_id', player_id)
        self.db_handler.update_data('test.player', 'points', 0, 'player_id', player_id)
        self.db_handler.update_data('test.player', 'answered_questions', 0, 'player_id', player_id)
    
    def get_questions_repetition(self, player_id):
        answers = self.db_handler.get_data_conditioned('test.answer', 'player_id', player_id, ['*'])
        questions = []
        for x in answers:
            if 'N' in x:
                questions.append(x[2])
        return questions
    
    def get_one_wrong_question(self, quest_id):
        question = self.db_handler.get_data_conditioned('test.sql_test', 'quest_id', quest_id, ['*'])
        return question
    
    def answer_execute(self, answer):
        result = self.db_handler.answer_execute(answer)
        return result
    
    def answer_checker(self, question_number, right_answer, user_answer):

        if user_answer == right_answer:
            pass