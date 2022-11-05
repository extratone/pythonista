#!python3

HELP = '''
The REPL keyboard allows you to use pretty much any text editing app as an interactive Python console.

Simply tap the '>>>' button, enter some Python code, then tap Eval.

The results of your code will be typed as text into any app you're using the keyboard with (e.g. Notes). Images and plots are shown within the keyboard (from where you can copy them to the clipboard).

Note: The REPL will not work properly in single-line text fields.
'''

import keyboard
import ui
import code
import sys
import io
import dialogs


def get_eval_line():
	before, after = keyboard.get_input_context()
	if before and (before.startswith('>>>') or before.startswith('...')):
		return before.strip()
	return ''


class REPLView (ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		self.input_buffer = ''
	
	def did_load(self):
		self['eval_button'].enabled = False
		self['eval_button'].action = self.eval_action
		self['help_button'].action = self.help_action
		self['cmd_button'].action = self.repl_button_action
		self.bg_color = '#143d58'
		self.tint_color = 'white'
		self.kb_text_changed()
		
	def kb_text_changed(self):
		line = get_eval_line()
		if line.startswith('>>>') or line.startswith('...'):
			self['label1'].text = line + '\nTap "Eval" to run this line.'
			self['eval_button'].enabled = True
		else:
			self['label1'].text = 'Tap ">>>" to start a REPL session or (?) for more information.'
			self['eval_button'].enabled = False
			
	def exec_line(self, line):
		keyboard.insert_text('\n')
		if self.input_buffer:
			line = self.input_buffer + line
		prev_stdout = sys.stdout
		redirected_out = io.StringIO()
		sys.stdout = redirected_out
		did_run = False
		try:
			c = code.compile_command(line, '<string>', 'single')
			if c is not None:
				exec(c, globals())
				did_run = True
			else:
				print('...   ', end='')
				self.input_buffer += line
		except Exception as e:
			print(f'{e.__class__.__name__}: {e}')
			# Note: If you'd prefer full tracebacks, you can un-comment the lines below:
			#import traceback
			#traceback.print_last(file=redirected_out)
			did_run = True
		finally:
			sys.stdout = prev_stdout
		output = redirected_out.getvalue()
		if len(output) > 1000:
			output = '[...]\n' + output[-1000:]
		keyboard.insert_text(output)
		if did_run:
			keyboard.insert_text('\n>>> ')
			self.input_buffer = ''
	
	def eval_action(self, sender):
		label = sender.superview['label1']
		label.text = keyboard.get_selected_text()
		line = get_eval_line()
		if line.startswith('>>> ') or line.startswith('... '):
			line = line[4:] + '\n'
			self.exec_line(line)
		else:
			label.text = 'Line is empty or does not start with ">>>"/"..."'

	def repl_button_action(self, sender):
		keyboard.insert_text('\n>>> ')
	
	def help_action(self, sender):
		tv = ui.TextView(editable=False, selectable=False)
		tv.font = ('<System>', 18)
		tv.text = HELP
		tv.name = 'About'
		tv.present()


def main():
	if keyboard.is_keyboard():
		v = ui.load_view('REPLView.pyui')
		keyboard.set_view(v, 'minimized')
	else:
		print('This script is meant to be run in the custom Pythonista Keyboard.')

if __name__ == '__main__':
	main()

