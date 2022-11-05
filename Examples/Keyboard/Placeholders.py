#!python3

'''
This script uses the included `faker` module to generate various formats of placeholder text, from 'Lorem Ipsum' to fake addresses and company names. If 'Full Access' is enabled for the Pythonista Keyboard, it can also download and show random placeholder images from picsum.photos. You can also run this in the main app.

Note: This script is primarily designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
import ui
import dialogs
import faker

def main():
	is_kb = keyboard.is_keyboard()
	full_access = keyboard.has_full_access()
	options = [{'title': 'Lorem Ipsum', 'key': 'lorem'}, {'title': 'The Quick Brown Fox...', 'key': 'pangram'}, {'title': 'Company Name', 'key': 'company'}, {'title': 'Catch Phrase', 'key': 'phrase'}, {'title': 'Name', 'key': 'name'}, {'title': 'Address', 'key': 'address'}, {'title': 'Random Cat Image (320x320)', 'key': 'image_320_320'}, {'title': 'Random Cat Image (640x480)', 'key': 'image_640_480'}, {'title': 'Example QR Code', 'key': 'qr'}]
	selected = dialogs.list_dialog('Placeholders...', options)
	if not selected:
		return
	n = selected['key']
	text = ''
	image_url = None
	image = None
	f = faker.Faker()
	if n == 'lorem':
		text = f.text()
	elif n == 'phrase':
		text = f.catch_phrase()
	elif n == 'company':
		text = f.company()
	elif n == 'name':
		text = f.name()
	elif n == 'address':
		text = f.address()
	elif n == 'pangram':
		text = 'The quick brown fox jumps over the lazy dog. 0123456789'
	elif n == 'qr':
		import qrcode
		image = qrcode.make('http://example.com')
	elif n.startswith('image_'):
		comps = n.split('_')
		w, h = int(comps[1]), int(comps[2])
		image_url = f'https://placekitten.com/{w}/{h}/?random'
		text = image_url
	if keyboard.is_keyboard():
		keyboard.insert_text(text)
	else:
		# For debugging in the main app:
		print('Keyboard input:\n', text)
	if image_url:
		if not is_kb or full_access:
			import requests
			r = requests.get(image_url)
			image = ui.Image.from_data(r.content)
		else:
			dialogs.hud_alert('Image download requires full access')
	if image:
		image.show()
	
if __name__ == '__main__':
	main()

