#!python3

'''
This shows a simple list of text replacements you've defined in the system-wide keyboard settings (Settings app).

Note: This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
import dialogs

def main():
	if not keyboard.is_keyboard():
		print('This script is meant to be run in the Pythonista keyboard.')
		return
	snippets = [s[0] for s in keyboard.get_text_replacements()]
	if len(snippets) == 0:
		dialogs.hud_alert('No Text Replacements')
		return
	selected = dialogs.list_dialog('Text Replacements', snippets)
	if selected:
		keyboard.insert_text(selected)

if __name__ == '__main__':
	main()

