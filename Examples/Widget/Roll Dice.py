#!python3

'''
This widget script shows a single button and a label.
Tapping the button simulates a dice roll and shows the result in the label.
'''

import appex, ui
import random

def roll_action(sender):
	symbols = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
	dice = [random.randint(1, 6) for i in range(2)]
	dice_str = ''.join(symbols[i - 1] for i in dice)
	sender.superview['result_label'].text = dice_str
	
v = ui.View(frame=(0, 0, 300, 110))
label = ui.Label(frame=(150, 0, 150, 110), flex='lwh', font=('<System>', 64), alignment=ui.ALIGN_CENTER, name='result_label')
v.add_subview(label)
button = ui.Button(title='Roll Dice!', font=('<System>', 24), flex='rwh', action=roll_action)
button.frame = (0, 0, 150, 110)
v.add_subview(button)

appex.set_widget_view(v)

