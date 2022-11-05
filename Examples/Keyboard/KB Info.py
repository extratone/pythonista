#!python3

'''
This is mostly just a helper script for better understanding the `keyboard` module.
It shows an info bar on top of the Pythonista Keyboards that updates automatically with the current input context (text before/after cursor) and selected text.
'''

import keyboard
import ui

class KeyboardInfoView (ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.background_color = '#00436e'
		self.label = ui.Label(frame=self.bounds.inset(0, 4, 0, 36), flex='WH')
		self.label.font = ('Menlo', 12)
		self.label.text_color = 'white'
		self.label.number_of_lines = 0
		self.add_subview(self.label)
		ui.delay(self.update_info, 0.5)
		
	def kb_text_changed(self):
		'''This gets called automatically by the keyboard (for the active view) whenever the text/selection changes'''
		self.update_info()
	
	def update_info(self):
		context = keyboard.get_input_context()
		selected = keyboard.get_selected_text()
		self.label.text = f'Input context: {context}\nSelection: "{selected}" ({len(selected)} characters)'

if __name__ == '__main__':
	v = KeyboardInfoView()
	keyboard.set_view(v)

