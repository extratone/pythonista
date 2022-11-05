#!python3
'''
This is mostly a demonstration of the new local notification capabilities in Pythonista 3.3, that allow you to schedule notifications with custom action buttons (quiz answers in this case), image attachments (not used here), and more.

The example also shows how to query a simple web API (Open Trivia DB) using Python.

As a challenge, you could try modifying this example to show one question per hour or per day. Or try to include a quiz category icon in the notification...
'''

import requests
import json
from urllib.parse import unquote
import time
import notification
import sys
import random
import ui
import dialogs
import appex
import shortcuts

def download_questions():
	print('Downloading questions from Open Trivia DB...')
	api_url = 'https://opentdb.com/api.php?amount=50&type=multiple&encode=url3986'
	r = requests.get(api_url)
	api_result = r.json()
	questions = api_result['results']
	processed_questions = []
	for q in questions:
		pq = {'category': unquote(q['category']),
		      'difficulty': unquote(q['difficulty']),
		      'question': unquote(q['question']),
		      'correct': unquote(q['correct_answer']),
		      'incorrect': [unquote(a) for a in q['incorrect_answers']]}
		processed_questions.append(pq)
	return processed_questions


def load_questions():
	# Load cached questions from disk if they have already been downloaded:
	try:
		with open('questions.json', 'r') as f:
			questions = json.load(f)
	except:
		questions = download_questions()
		with open('questions.json', 'w') as f:
			json.dump(questions, f, indent=2)
	return questions


def ask_question(questions, i, points=0, prefix='', delay=0, sound_name=None):
	q = questions[i]
	all_answers = [q['correct']] + q['incorrect']
	random.shuffle(all_answers)
	notif_actions = []
	# Generate a pythonista:// (action) URL for every possible answer:
	base_url = shortcuts.pythonista_url(sys.argv[0], action='run')
	for a in all_answers:
		is_correct = a == q['correct']
		url = base_url + '&argv=' + ('correct' if is_correct else 'incorrect')
		url += '&argv=%i' % (i+1,) # Next question index
		url += '&argv=%i' % (points,)
		notif_actions.append({'title': a, 'action_url': url})
	main_action_url = base_url + '&argv=ask&argv=%i&argv=%i' % (i, points)
	notification.schedule(title='Quiz - Question %i (%s)' % (i+1, q['category']), delay=delay,
	                      subtitle=prefix + ' [ %i Points ]' % (points,),
	                      message=q['question'],
	                      action_url=main_action_url,
	                      actions=notif_actions,
	                      attachments=None,
	                      sound_name=sound_name,
	                      identifier='PythonistaQuiz')


def show_summary(points):
	notification.schedule(title='Quiz', delay=1, message=f'You have reached {points} points. Congratulations! 🎉', sound_name='drums:Drums_11', identifier='PythonistaQuiz')


def ask_question_in_app(questions, i, points=0):
	# When the notification is activated without an answer button, ask the question again using an in-app dialog:
	q = questions[i]
	all_answers = [q['correct']] + q['incorrect']
	random.shuffle(all_answers)
	answer_fields = [{'title': a, 'type': 'check', 'group': 'answer'} for a in all_answers]
	footer = 'Question %i -- You have %i points' % (i+1, points)
	result = dialogs.form_dialog('Quiz', sections=[(q['question'], answer_fields, footer)])
	if result:
		if result['answer'] == q['correct']:
			points += 100
			ask_question(questions, i+1, delay=1, points=points, sound_name='game:Ding_3', prefix='✅ Correct! ')
		else:
			ask_question(questions, i+1, delay=1, points=points, sound_name='game:Error', prefix='❌ Wrong! ')


def main():
	args = sys.argv[1:]
	if not args:
		# Running in foreground, show instructions first...
		dialogs.alert('Instructions', 'This game can be played entirely in Notification Center.\n\nYou will get each question as a notification, so make sure that "Do not Disturb" is not enabled.\n\nYou can answer questions directly in Notification Center by tapping and holding the notification (or using 3D Touch, if your device supports it). This will show the multiple-choice options.\n\nThe next question will be shown automatically after you answer. There are 10 questions in total.', 'Start Game')
	questions = load_questions()
	if len(args) >= 3:
		# NOTE: Cmd line arguments (except for script path) are: [correct/incorrect/ask] [question_index] [points]
		task = args[0]
		next_q = int(args[1])
		points = int(args[2])
		at_end = next_q > 3
		if task == 'correct':
			points += 100
			if not at_end:
				ask_question(questions, next_q, delay=1, points=points, sound_name='game:Ding_3', prefix='✅ Correct! ')
		elif task == 'incorrect':
			if not at_end:
				ask_question(questions, next_q, delay=1, points=points, sound_name='game:Error', prefix='❌ Wrong! ')
		if task == 'ask':
			ask_question_in_app(questions, next_q, points)
		elif at_end:
			show_summary(points)
			
	else:
		# Start a new quiz:
		# Challenge: It might be even more interesting to schedule a daily quiz at this point (with an option to unschedule it)...
		ask_question(questions, 0, points=0, sound_name='game:Ding_3', delay=0)

if __name__ == '__main__':
	main()

