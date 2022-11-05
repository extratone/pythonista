#!python3

'''
This script allows you to apply various text effects to any text you type with the Pythonista Keyboard.
You can easily add additional text effects, simply by writing a single "transform" function, and adding an entry to a dictionary (see comments in the code).

Note: This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
import ui
import codecs
from urllib.parse import quote
from random import random, choice, randint
import faker


def no_effect(text):
	return text


def url_encode_effect(text):
	return quote(text, '')


def rot13_effect(text):
	# This is a very simple obfuscation scheme that can be reversed with the same function. It is not real encryption, but you could not read it at a glance. After you've typed your garbled text, you can select it, and tap the 'transform' button to translate it back to normal text.
	return codecs.encode(text, 'rot13')


f = faker.Faker()
lorem_ipsum = None
lorem_ipsum_index = 0

def lorem_ipsum_effect(text):
	global lorem_ipsum, lorem_ipsum_index
	if lorem_ipsum is None:		
		lorem_ipsum = f.text(1000)
	if text in ('\n', ' ', ',', '.', '!', '?'):
		return text
	result = ''
	for i in range(len(text)):
		result += lorem_ipsum[lorem_ipsum_index]
		lorem_ipsum_index += 1
		if lorem_ipsum_index >= len(lorem_ipsum):
			lorem_ipsum_index = 0
	result = result.replace('\n', ' ')
	return result


flipped_letters = {
	'a': '\u0250', 'b': 'q', 'c': '\u0254', 'd': 'p', 'e': '\u01DD',
	'f': '\u025F', 'g': '\u0183', 'h': '\u0265', 'i': '\u0131',
	'j': '\u027E', 'k': '\u029E', 'm': '\u026F', 'n': 'u', 'p': 'd',
	'q': 'b', 'r': '\u0279', 't': '\u0287', 'u': 'n', 'v': '\u028C',
	'w': '\u028D', 'y': '\u028E', '.': '\u02D9', '[': ']', '(': ')',
	'{': '}', '?': '\u00BF', '!': '\u00A1', '\'': ',', '<': '>',
	'_': '\u203E', '\u203F': '\u2040', '\u2045': '\u2046',
	'\u2234': '\u2235'
}

def flip_effect(text):
	rev_text = ''.join(reversed(text))
	return ''.join(flipped_letters.get(c.lower(), c) for c in rev_text)


def underline_effect(text):
	return ''.join(c + '\u0332' for c in text)


def spongebob_effect(text):
	return ''.join(c.upper() if random() > 0.5 else c.lower() for c in text)


zalgo = ['\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305',
	'\u0306', '\u0307', '\u0308', '\u0309', '\u030A', '\u030B', '\u030C',
	'\u030D', '\u030E', '\u030F', '\u0310', '\u0311', '\u0312', '\u0313',
	'\u0314', '\u0315', '\u031A', '\u031B', '\u033D', '\u033E', '\u033F',
	'\u0340', '\u0341', '\u0342', '\u0343', '\u0344', '\u0346', '\u034A',
	'\u034B', '\u034C', '\u0350', '\u0351', '\u0352', '\u0357', '\u0358',
	'\u035B', '\u035D', '\u035E', '\u0360', '\u0361', '\u0316', '\u0317',
	'\u0318', '\u0319', '\u031C', '\u031D', '\u031E', '\u031F', '\u0320',
	'\u0321', '\u0322', '\u0323', '\u0324', '\u0325', '\u0326', '\u0327',
	'\u0328', '\u0329', '\u032A', '\u032B', '\u032C', '\u032D', '\u032E',
	'\u032F', '\u0330', '\u0331', '\u0332', '\u0333', '\u0339', '\u033A',
	'\u033B', '\u033C', '\u0345', '\u0347', '\u0348', '\u0349', '\u034D',
	'\u034E', '\u0353', '\u0354', '\u0355', '\u0356', '\u0359', '\u035A',
	'\u035C', '\u035F', '\u0362', '\u0334', '\u0335', '\u0336', '\u0337',
	'\u0338', '\u0363', '\u0364', '\u0365', '\u0366', '\u0367', '\u0368',
	'\u0369', '\u036A', '\u036B', '\u036C', '\u036D', '\u036E', '\u036F'
]

def zalgo_effect(text):
	result = ''
	for c in text:
		result += c
		if c in (' ', '\n'):
			continue
		for i in range(randint(3, 12)):
			m = choice(zalgo)
			result += m
	return result


def obfuscate_html_effect(text):
	if text in ('\n', '\t'):
		return text
	return ''.join('&#' + hex(ord(c))[1:] + ';' for c in text)


# --- How to add your own effects:
# Simply define a function that takes a single parameter (the entered text) and returns the result of your transformation.
# Then add an entry to the `effects` list below, so that it gets shown in the UI. You can also remove effects you don't like, of course.

effects = [
	{'title': 'None', 'func': no_effect},
	{'title': 'Flip', 'func': flip_effect, 'rtl': True},
	{'title': 'Underline', 'func': underline_effect},
	{'title': 'URL', 'func': url_encode_effect},
	{'title': 'ROT13', 'func': rot13_effect},
	{'title': 'L. Ipsum', 'func': lorem_ipsum_effect},
	{'title': 'sPoNgEbOb', 'func': spongebob_effect},
	{'title': 'Zalgo', 'func': zalgo_effect},
	{'title': 'Obf. HTML', 'func': obfuscate_html_effect}
]


class TextEffectsView (ui.View):
	'''This custom view class implements a simple UI for selecting the current text effect from a segmented control, and a button for transforming the selected text. By setting it as the Pythonista keyboard's accessory view via `keyboard.set_view()`, it receives callbacks for all key presses (on the on-screen keyboard), so that the selected transformation function can be called before the character is entered.
	'''
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.background_color = 'white'
		scroll_view = ui.ScrollView(frame=self.bounds.inset(0, 0, 0, 80), flex='wh')
		h = scroll_view.bounds.h
		seg_w = len(effects) * 80
		scroll_view.content_size = (seg_w + 8, 0)
		scroll_view.shows_horizontal_scroll_indicator = False
		self.add_subview(scroll_view)
		
		mode_ctrl = ui.SegmentedControl(frame=(2, 2, seg_w, h - 4), flex='h')
		mode_ctrl.segments = [effect['title'] for effect in effects]
		mode_ctrl.selected_index = 0
		scroll_view.add_subview(mode_ctrl)
		self.mode_ctrl = mode_ctrl
		
		transform_button = ui.Button(frame=(scroll_view.frame.max_x, 0, 44, h), flex='hl')
		transform_button.image = ui.Image('iow:arrow_swap_24')
		transform_button.action = self.transform_action
		self.add_subview(transform_button)
	
	def transform_action(self, sender):
		'''This is bound to the "transform" button that applies the current
		text filter to the selected text.'''
		selected_text = keyboard.get_selected_text()
		if not selected_text:
			return
		lines = selected_text.splitlines()
		if len(lines) > 1:
			# NOTE: The return value of `keyboard.get_selected_text()` may not include all text for selections that are longer than one line (or about ~1000 characters). Unfortunately, it is not possible to change this, as it's a system limitation. In order to avoid accidentally deleting text, we don't replace selections that are more than one line.
			import dialogs
			dialogs.hud_alert('Select less text')
			return
		effect = effects[self.mode_ctrl.selected_index]
		func = effect['func']
		transformed = func(selected_text)
		if transformed:
			keyboard.insert_text(transformed)
	
	def kb_should_insert(self, text=''):
		'''This gets called automatically by the keyboard for the active view.
		It lets your view decide which key presses to accept, and which to filter.'''
		# Check which effect is active:
		effect = effects[self.mode_ctrl.selected_index]
		func = effect['func']
		rtl = effect.get('rtl', False)
		# Apply the active effect:
		transformed = func(text)
		if transformed:
			keyboard.insert_text(transformed)
			if rtl and text != '\n':
				# The rtl (right-to-left) mode is only used for the 'Flipped' effect.
				keyboard.move_cursor(-1)
			return False
		else:
			return True


if __name__ == '__main__':
	v = TextEffectsView()
	if keyboard.is_keyboard():
		# This keyboard view requires the QWERTY keyboard to be visible,
		# so the view is set in 'minimized' mode.
		keyboard.set_view(v, 'minimized')
	else:
		# For debugging in the main app:
		v.frame = (0, 0, 350, 40)
		v.name = 'Keyboard Preview'
		v.present('sheet')

