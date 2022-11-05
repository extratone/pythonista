#!python3

HELP = '''
The calculator uses the text you're editing with the Pythonista Keyboard as input. For example, You can type a line like "6*sin(pi)" or "6*7" in the Notes app, and the keyboard automatically shows the live results in a line above the QWERTY keys. You can use everything from the `math` and `random` modules without prefix (they're star-imported).

You can tap the up-arrow button to insert the result in your document. If text is selected, it is replaced by the plain result, otherwise "= [result]" is entered.

Note: This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
import ui
from math import *
from random import *
import faker

fake = faker.Faker()


class CalculatorView (ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		w, h = self.bounds.size
		self.background_color = '#005b00'
		self.label = ui.Label(frame=self.bounds.inset(0, 4, 0, 36+40), flex='wh')
		self.label.text_color = 'white'
		self.label.font = ('Chalkboard SE', 18)
		self.label.number_of_lines = 0
		self.add_subview(self.label)
		self.insert_button = ui.Button(frame=(w-80, 0, 40, h), flex='hl')
		self.insert_button.image = ui.Image('iow:arrow_up_c_32')
		self.insert_button.tint_color = 'white'
		self.insert_button.enabled = False
		self.insert_button.action = self.insert_action
		self.add_subview(self.insert_button)
		self.help_button = ui.Button(frame=(w-120, 0, 40, h), flex='hl')
		self.help_button.image = ui.Image('iow:help_circled_32')
		self.help_button.tint_color = 'white'
		self.help_button.action = self.help_action
		self.add_subview(self.help_button)
		self.result = None
		self.kb_text_changed()
	
	def insert_action(self, sender):
		if keyboard.get_selected_text():
			keyboard.insert_text(self.result)
		else:
			keyboard.insert_text(' = ' + self.result)
	
	def help_action(self, sender):
		tv = ui.TextView(editable=False, selectable=False)
		tv.font = ('<System>', 18)
		tv.text = HELP
		tv.name = 'About'
		tv.present()
	
	def kb_text_changed(self):
		text = keyboard.get_selected_text()
		if not text:
			text = keyboard.get_input_context()[0]
		text = text.strip() if text else ''
		if not text:
			self.label.text = '(Nothing Selected)'
			self.insert_button.enabled = False
			return
		if ':' in text:
			# Ignore leading label, separated by colon
			text = text.split(':', 1)[1]
		try:
			self.result = str(eval(text, globals(), locals()))
			self.label.text = f'{text} = {self.result}'
			self.insert_button.enabled = True
		except:
			self.label.text = '(No Expression Selected)'
			self.insert_button.enabled = False


def main():
	v = CalculatorView()
	if keyboard.is_keyboard():
		keyboard.set_view(v, 'minimized')
	else:
		print('This script is meant to be run in the Pythonista keyboard.')

if __name__ == '__main__':
	main()
	
