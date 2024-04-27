import sys
import time
from PIL import Image
from inky.auto import auto
import os

while(1):
	os.system("python3 /home/umair/Documents/info_dashboard/weather.py")
	inky = auto(ask_user=True, verbose=True)
	saturation = 0.5

	image = Image.open('/home/umair/Documents/info_dashboard/weather.png')
	resizedimage = image.resize(inky.resolution)


	inky.set_image(resizedimage, saturation=saturation)
	inky.show()
	
	time.sleep(3600)
