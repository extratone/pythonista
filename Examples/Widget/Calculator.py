#!python3

'''
This script implements a simple calculator in the Today widget.

You can toggle between two different button layouts (compact/expanded) using the widget's
built-in "Show More/Less" button. This is accomplished by overriding the `ui.View.layout`
method in the `CalcView` class.
'''

import appex, ui
import console
import os

op_symbols = ('+', '\u2212', '\u00F7', '\u00D7')
operators = {'+': '+', '\u2212': '-', '\u00F7': '/', '\u00D7': '*'}

class CalcView (ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.shows_result = False
		self.bounds = (0, 0, 400, 200)
		button_style = {'background_color': (0, 0, 0, 0.05), 'tint_color': 'black', 'font': ('HelveticaNeue-Light', 24), 'corner_radius': 3}
		self.number_buttons = [ui.Button(title=str(i), action=self.button_tapped, **button_style) for i in range(10)]
		self.op_buttons = [ui.Button(title=s, action=self.button_tapped, **button_style) for s in op_symbols]
		self.ac_button = ui.Button(title='AC', action=self.button_tapped, **button_style)
		self.ac_button.tint_color = 'red'
		self.add_subview(self.ac_button)
		self.c_button = ui.Button(title='C', action=self.button_tapped, **button_style)
		self.c_button.tint_color = 'red'
		self.add_subview(self.c_button)
		self.eq_button = ui.Button(title='=', action=self.button_tapped, **button_style)
		self.add_subview(self.eq_button)
		self.dot_button = ui.Button(title='.', action=self.button_tapped, **button_style)
		self.add_subview(self.dot_button)
		for b in self.number_buttons + self.op_buttons:
			self.add_subview(b)
		self.display_view = ui.View(background_color=(.54, .94, 1.0, 0.2))
		self.display_label = ui.Label(frame=self.display_view.bounds.inset(0, 8), flex='wh', text='0', alignment=ui.ALIGN_RIGHT)
		self.display_label.font = ('HelveticaNeue-Light', 32)
		self.display_view.add_subview(self.display_label)
		self.add_subview(self.display_view)
	
	def layout(self):
		compact = self.height < 150
		bw = self.width / 10 if compact else self.width / 5
		bh = self.height / 3 if compact else self.height / 5
		for i, b in enumerate(self.number_buttons):
			if compact:
				frame = ui.Rect(((i - 1) % 10) * bw, bh, bw, bh)
			else:
				frame = ui.Rect(max(i-1, 0) % 3 * bw, 3 * bh - (i-1) // 3 * bh, bw, bh)
			b.frame = frame.inset(1, 1)
		for i, b in enumerate(self.op_buttons):
			if compact:
				frame = ui.Rect((4 + i) * bw, 2 * bh, bw, bh)
			else:
				frame = ui.Rect((3 + i % 2) * bw, (2 + i//2) * bh, bw, bh)
			b.frame = frame.inset(1, 1)
		if compact:
			self.ac_button.frame = ui.Rect(0, 2 * bh, 2 * bw, bh).inset(1, 1)
			self.c_button.frame = ui.Rect(2 * bw, 2 * bh, bw, bh).inset(1, 1)
			self.eq_button.frame = ui.Rect(8 * bw, 2 * bh, 2*bw, bh).inset(1, 1)
			self.dot_button.frame = ui.Rect(3 * bw, 2 * bh, bw, bh).inset(1, 1)
		else:
			self.ac_button.frame = ui.Rect(3 * bw, bh, bw, bh).inset(1, 1)
			self.c_button.frame = ui.Rect(4 * bw, bh, bw, bh).inset(1, 1)
			self.eq_button.frame = ui.Rect(3 * bw, 4 * bh, 2*bw, bh).inset(1, 1)
			self.dot_button.frame = ui.Rect(bw, 4 * bh, bw, bh).inset(1, 1)
		self.display_view.frame = (0, 0, self.width, bh)
	
	def button_tapped(self, sender):
		t = sender.title
		label = self.display_label
		if t in '0123456789':
			if self.shows_result or label.text == '0':
				label.text = t
			else:
				label.text += t
		elif t == '.' and label.text[-1] != '.':
			label.text += t
		elif t in op_symbols:
			if label.text[-1] in op_symbols:
				label.text = label.text[:-1] + t
			else:
				label.text += t
		elif t == 'AC':
			label.text = '0'
		elif t == 'C':
			label.text = label.text[:-1]
			if len(label.text) == 0:
				label.text = '0'
		elif t == '=':
			try:
				expr = label.text
				for symbol in op_symbols:
					expr = expr.replace(symbol, operators[symbol])
				result = str(eval(expr))
				if result.endswith('.0'):
					result = result[:-2]
				label.text = result
			except (SyntaxError, ZeroDivisionError):
				label.text = 'ERROR'
			self.shows_result = True
		if t != '=':
			self.shows_result = False

def main():
	# Optimization: Don't create a new view if the widget already shows the calculator.
	widget_name = __file__ + str(os.stat(__file__).st_mtime)
	widget_view = appex.get_widget_view()
	if widget_view is None or widget_view.name != widget_name:
		widget_view = CalcView()
		widget_view.name = widget_name
		appex.set_widget_view(widget_view)

if __name__ == '__main__':
	main()
