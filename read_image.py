#to get the image downloaded: 
import shutil

import requests
def get_image():
	url = "http://localhost:5000/images"
	new_url = requests.get(url)
	new_url = new_url.content.decode('utf-8')
	response = requests.get(new_url, stream=True)
	with open('face.png', 'wb') as out_file:
	    shutil.copyfileobj(response.raw, out_file)

if __name__ == '__main__':
	get_image()