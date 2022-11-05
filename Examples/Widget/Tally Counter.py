#!python3

'''
This widget script implements a "tally counter".
The current counter value is persisted to a file, so it can be restored when the widget is restarted.
'''

import appex, ui, os

counter = 0
# Try to load previous counter value from file:
try:
	with open('.TallyCounter.txt') as f:
		counter = int(f.read())
except IOError:
	pass

def button_tapped(sender):
	# Update the counter, depending on which button was tapped:
	global counter
	if sender.name == '+':
		counter += 1
	elif sender.name == '-':
		counter = max(0, counter - 1)
	elif sender.name == 'reset':
		counter = 0
	# Update the label:
	sender.superview['text_label'].text = str(counter)
	# Save the new counter value to a file:
	with open('.TallyCounter.txt', 'w') as f:
		f.write(str(counter))

def main():
	# Optimization: Don't create a new view if the widget already shows the tally counter.
	widget_name = __file__ + str(os.stat(__file__).st_mtime)
	v = appex.get_widget_view()
	if v is not None and v.name == widget_name:
		return
	v = ui.View(frame=(0, 0, 320, 64), name=widget_name)
	label = ui.Label(frame=(0, 0, 320-44, 64), flex='wh', font=('HelveticaNeue-Light', 64), alignment=ui.ALIGN_CENTER, text=str(counter))
	label.name = 'text_label'
	v.add_subview(label)
	minus_btn = ui.Button(name='-', image=ui.Image('iow:ios7_minus_outline_32'), flex='hl', tint_color='#666', action=button_tapped)
	minus_btn.frame = (320-128, 0, 64, 64)
	v.add_subview(minus_btn)
	plus_btn = ui.Button(name='+', image=ui.Image('iow:ios7_plus_outline_32'), flex='hl', tint_color='#666', action=button_tapped)
	plus_btn.frame = (320-64, 0, 64, 64)
	v.add_subview(plus_btn)
	reset_btn = ui.Button(name='reset', image=ui.Image('iow:ios7_skipbackward_outline_32'), flex='h', tint_color='#666', action=button_tapped)
	reset_btn.frame = (0, 0, 64, 64)
	v.add_subview(reset_btn)
	appex.set_widget_view(v)

if __name__ == '__main__':
	main()
	
