#!python3

'''
This custom keyboard script implements a simple emoji search. While the search view is active, all keyboard input (from the on-screen qwerty keyboard) is redirected to the search field, and not typed in the app. You can simply close (x) the view to resume typing normally.

This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
import emoji
import ui
from operator import itemgetter
all_emoji = emoji.core.unicode_codes.EMOJI_UNICODE

class EmojiSearchView (ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.frame = (0, 0, 320, 40)
		self.background_color = 'white'
		self.label = ui.Label(frame=(40, 0, 120, self.bounds.h), flex='h')
		self.label.font = ('<System-Bold>', 15)
		self.label.line_break_mode = ui.LB_TRUNCATE_MIDDLE
		self.label.text = 'Type to search'
		self.is_empty = True
		self.add_subview(self.label)
		self.search_icon_view = ui.ImageView(frame=(0, 0, 40, self.bounds.h), flex='hr')
		search_icon = ui.Image('iow:ios7_search_strong_32').with_rendering_mode(ui.RENDERING_MODE_TEMPLATE)
		self.search_icon_view.image = search_icon
		self.search_icon_view.content_mode = ui.CONTENT_CENTER
		self.search_icon_view.tint_color = (0.5, 0.5, 0.5, 0.5)
		#TODO: Clear text button
		self.add_subview(self.search_icon_view)
		self.scroll_view = ui.ScrollView(frame=(160, 0, self.bounds.w - 160 - 36, self.bounds.h))
		self.scroll_view.flex = 'wh'
		self.scroll_view.shows_horizontal_scroll_indicator = False
		self.add_subview(self.scroll_view)
		self.emoji_buttons = []
	
	def kb_should_insert(self, text=''):
		if text in ('\n', ' '):
			return True
		if self.is_empty:
			self.label.text = text
			self.is_empty = False
		else:
			self.label.text += text
		self.update_search()
		return False
	
	def kb_should_delete(self):
		self.label.text = self.label.text[:-1]
		self.update_search()
		return False
	
	def emoji_button_action(self, sender):
		text = sender.title
		keyboard.insert_text(text)
	
	def update_search(self):
		text = self.label.text
		if not text:
			self.is_empty = True
			self.label.text = 'Type to search'
		matches = []
		for name in all_emoji:
			try:
				i = name.lower().index(text.lower())
				matches.append((i, all_emoji.get(name)))
			except ValueError:
				pass
		matches.sort(key=itemgetter(0))
		# Show 10 results at most
		matches = matches[:10]
		for button in self.emoji_buttons:
			self.scroll_view.remove_subview(button)
		self.buttons = []
		if not text:
			return
		x = 4
		h = self.bounds.h
		for m in matches:
			text = m[1]
			button = ui.Button(frame=(x, 2, 40, h-4))
			button.flex = 'h'
			button.title = text
			button.corner_radius = 4
			button.background_color = (0.5, 0.5, 0.5, 0.1)
			button.font = ('<System>', 20)
			button.action = self.emoji_button_action
			self.scroll_view.add_subview(button)
			self.emoji_buttons.append(button)
			x += 44
		self.scroll_view.content_size = (len(matches) * 44 + 4, 0)

def main():
	v = EmojiSearchView()
	keyboard.set_view(v, 'minimized')

if __name__ == '__main__':
	main()

