#!python3

import keyboard
import ui
import random
import itertools

EMOJI = ['▫️', '🔥', '🐶', '💦', '😍', '🌟', '🌈', '🐍', '🎉', '❤️', '💚', '💥', '💨', '⬇️', '⬆️️']

class EmojiCanvasView (ui.View):
	def __init__(self, *args, cols=9, rows=8, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.background_color = 'white'
		self.cols = cols
		self.rows = rows
		self.labels = []
		self.brush = EMOJI[1]
		for i in range(cols * rows):
			label = ui.Label()
			label.text = EMOJI[0]
			label.alignment = ui.ALIGN_CENTER
			label.font = ('<System>', 20)
			label.scales_font = True
			label.min_font_scale = 0.2
			self.add_subview(label)
			self.labels.append(label)
	
	def label_for_touch(self, touch):
		s = self.bounds.h / self.rows
		x = max(0, min(self.cols-1, int(touch.location.x / s)))
		y = max(0, min(self.rows-1, int(touch.location.y / s)))
		label = self.labels[x + y * self.cols]
		return label
	
	def touch_began(self, touch):
		label = self.label_for_touch(touch)
		label.text = self.brush
	
	def touch_moved(self, touch):
		label = self.label_for_touch(touch)
		label.text = self.brush
	
	def layout(self):
		s = self.bounds.h / self.rows
		for i, label in enumerate(self.labels):
			x = i % self.cols
			y = i // self.cols
			self.labels[i].frame = (x*s, y*s, s, s)


class EmojiPaintView (ui.View):
	def __init__(self, *args, cols=9, rows=8, **kwargs):
		super().__init__(self, *args, **kwargs)
		w, h = self.bounds.size
		self.background_color = '#fafafa'
		self.palette_view = ui.ScrollView(frame=(2, 2, 40, h - 4), flex='h')
		self.palette_view.shows_vertical_scroll_indicator = False
		self.palette_view.background_color = '#eee'
		self.palette_view.corner_radius = 5
		self.add_subview(self.palette_view)
		self.canvas_view = EmojiCanvasView(frame=self.bounds, cols=cols, rows=rows, flex='wh')
		self.add_subview(self.canvas_view)
		self.copy_button = ui.Button(frame=(w - 42, h - 2 - 42 - 40, 40, 40), flex='lt')
		self.copy_button.image = ui.Image('iow:clipboard_32')
		self.copy_button.action = self.copy_action
		self.add_subview(self.copy_button)
		self.input_button = ui.Button(frame=(w - 42, h - 42, 40, 40), flex='lt')
		self.input_button.image = ui.Image('iow:arrow_up_c_32')
		self.input_button.action = self.input_action
		self.add_subview(self.input_button)
		self.palette_view.content_size = (0, 40 * len(EMOJI))
		self.emoji_buttons = []
		y = 0
		for e in EMOJI:
			button = ui.Button()
			button.frame = (0, y, 40, 40)
			button.title = e
			button.border_color = '#ccc'
			button.corner_radius = 4
			button.action = self.brush_action
			self.palette_view.add_subview(button)
			self.emoji_buttons.append(button)
			y += 40
		self.update_brush_selection()
	
	def brush_action(self, sender):
		keyboard.play_input_click()
		self.canvas_view.brush = sender.title
		self.update_brush_selection()

	def generate_text(self):
		col = 0
		text = '\n'
		for label in self.canvas_view.labels:
			text += label.text
			col += 1
			if col >= self.canvas_view.cols:
				col = 0
				text += '\n'
		return text

	def copy_action(self, sender):
		import dialogs
		if not keyboard.has_full_access():
			dialogs.hud_alert('Clipboard requires full access')
			return
		import clipboard
		clipboard.set(self.generate_text())
		dialogs.hud_alert('Copied')
	
	def input_action(self, sender):
		keyboard.insert_text(self.generate_text())
	
	def update_brush_selection(self):
		brush = self.canvas_view.brush
		for button in self.emoji_buttons:
			if button.title == brush:
				button.border_width = 1
			else:
				button.border_width = 0
		

	def layout(self):
		w, h = self.bounds.size
		s = h / self.canvas_view.rows
		canvas_w = s * self.canvas_view.cols
		canvas_frame = self.bounds.inset(0, (w - canvas_w)/2, 0, (w - canvas_w)/2)
		canvas_frame = canvas_frame.inset(2, 2, 2, 2)
		self.canvas_view.frame = canvas_frame
	

def main():
	v = EmojiPaintView()
	if keyboard.is_keyboard():
		v.name = 'Emoji Paint'
		keyboard.set_view(v, 'expanded')
	else:
		v.name = 'Keyboard Preview'
		v.frame = (0, 0, 320, 220)
		v.present('sheet')

if __name__ == '__main__':
	main()

