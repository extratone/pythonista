#!python3

'''
This script generates a QR code from the selected text. If 'Full Access' is enabled for the Pythonista Keyboard, you can also copy the resulting image to the clipboard.

Note: This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
import qrcode
import dialogs

if keyboard.is_keyboard():
	text = keyboard.get_selected_text()
else:
	# Use sample text for testing in main app
	text = 'http://pythonista-app.com'

if text:
	img = qrcode.make(text)
	img.show()
else:
	dialogs.hud_alert('No text selected', 'error')

