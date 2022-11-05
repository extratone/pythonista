#!python3

'''
This RGB/HSV color mixer runs in the Pythonista keyboard, and lets you insert and modify hex (html) colors in any app that can edit text. The GUI is mostly defined in the associated 'Colors.pyui' file that is required to run this.

This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the "Shortcuts..." option in the 'wrench' menu for more information.
'''

import ui
import keyboard
import colorsys

class ColorsView (ui.View):
	
	def did_load(self):
		self.background_color = 'white'
		# Bind actions for the sliders and buttons:
		self['slider1'].action = self.slider_action
		self['slider2'].action = self.slider_action
		self['slider3'].action = self.slider_action
		self['mode_ctrl'].action = self.mode_action
		self['copy_button'].action = self.copy_action
		self['insert_button'].action = self.insert_action
		# Initialize the current color:
		self.slider_action(None)
	
	def mode_action(self, sender):
		# Called when the RGB/HSV control changes its value
		mode = sender.selected_index
		self.slider_action(None)
		if mode == 0:
			self['label1'].text = 'R'
			self['label2'].text = 'G'
			self['label3'].text = 'B'
		else:
			self['label1'].text = 'H'
			self['label2'].text = 'S'
			self['label3'].text = 'V'
	
	def copy_action(self, sender):
		# Called when the 'Copy' button is tapped
		if keyboard.has_full_access():
			import clipboard, dialogs
			clipboard.set(self['hex_label'].text)
			dialogs.hud_alert('Copied')
		else:
			# The clipboard is not available if the keyboard does not have full access.
			import dialogs
			dialogs.hud_alert('Clipboard requires full access')
	
	def insert_action(self, sender):
		# Called when the 'Insert' button is tapped
		text = self['hex_label'].text
		if keyboard.is_keyboard():
			keyboard.insert_text(text)
		else:
			# For debugging in the main app:
			print('Keyboard input:', text)
		
	def slider_action(self, sender):
		s1 = self['slider1'].value
		s2 = self['slider2'].value
		s3 = self['slider3'].value
		sliders = (s1, s2, s3)
		mode = self['mode_ctrl'].selected_index
		if mode == 0:
			# RGB
			rgb = sliders
		else:
			# HSV mode, convert the color to RGB first
			rgb = colorsys.hsv_to_rgb(*sliders)
		self['swatch'].background_color = rgb
		# Update the hex label:
		rgb_256 = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
		rgb_hex = '#%02x%02x%02x' % rgb_256
		self['hex_label'].text = rgb_hex
	
	def set_color_from_text(self, text):
		# Try to parse the selected text as a color, and update the sliders accordingly.
		# This works both for hex colors (e.g. '#ff00cc') and color names (e.g. 'red')
		if not text:
			return
		parsed_color = ui.parse_color(text)
		if not any(parsed_color):
			return
		self['swatch'].background_color = parsed_color
		r, g, b, a = parsed_color
		mode = self['mode_ctrl'].selected_index
		if mode == 0:
			self['slider1'].value = r
			self['slider2'].value = g
			self['slider3'].value = b
		else:
			h, s, v = colorsys.rgb_to_hsv(r, g, b)
			self['slider1'].value = h
			self['slider2'].value = s
			self['slider3'].value = v
		self.slider_action(None)
	
	def kb_text_changed(self):
		# This gets called automatically by the keyboard when text and/or selection in the document changes.
		# We're using this to update the color from the selected text here.
		selected = keyboard.get_selected_text()
		if not selected:
			return
		self.set_color_from_text(selected)


def main():
	v = ui.load_view('Colors.pyui')
	if keyboard.is_keyboard():
		keyboard.set_view(v, 'expanded')
	else:
		# For debugging in the main app:
		v.name = 'Keyboard Preview'
		v.present('sheet')

if __name__ == '__main__':
	main()


