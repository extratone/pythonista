#!python3

'''
This is one of the simplest examples for the Pythonista Keyboard. It just inserts the current date and time in the document in whatever app you're using to edit text.

You can easily modify the date/time fomat by changing the `date_format` string below.

Note: This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
from datetime import datetime

date_format = '%Y-%m-%d %H:%M'

now = datetime.now()
date_str = now.strftime(date_format)
if keyboard.is_keyboard():
	keyboard.play_input_click()
	keyboard.insert_text(date_str)
else:
	# For debugging in the main app:
	print(f'Keyboard input: {date_str}')

