import cv2
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

import imageio
import os
import sys

# This function blends two images together by creating a series of len intermediate images
# with incremental alpha changes.  It uses the OpenCV function addWeighted for alpha blending.  
# https://stackoverflow.com/questions/28650721/cv2-python-image-blending-fade-transition
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html
def fadeIn (img1, img2, len=10, prefix=0): #pass images here to fade between
	for IN in range(0,len):
		fadein = IN/float(len)
		dst = cv2.addWeighted( img1, 1-fadein, img2, fadein, 0)
		cv2.imshow('window', dst)
		cv2.waitKey(1)
		print fadein
		# Save the image with a unique name that will sort approporiately alphabetically
		cv2.imwrite("output/"+str(prefix)+str(IN).zfill(3)+".jpg", dst)

# This function will read 4 images, named Dice1.JPG...Dice4.JPG and subsample them down to
# an image 12.5% of the original.  It will then call fadeIn() on each of the adjoining images, 
# including the last and first image
def fade_dice():
	dice_images = []
	prefix = 0
	for i in range(1,5):
		dice_images.append(cv2.imread("Dice"+str(i)+".JPG", cv2.IMREAD_COLOR)[::8,::8,::])
	for j,k in zip(dice_images[:-1], dice_images[1:]):
		fadeIn(j, k, 40, prefix)
		prefix+=1
	fadeIn(dice_images[-1], dice_images[0], 40, prefix)

# This function will read all JPEG or PNG files in the "input" directory, sort them alphabetically
# by name, and then combine them into an animated GIF using imageIO.
# https://stackoverflow.com/questions/38433425/custom-frame-duration-for-animated-gif-in-python-imageio
# http://imageio.readthedocs.io/en/latest/userapi.html
def gen_gif():
	frames = []
	image_files = sorted(os.listdir("input"))
	for img in image_files:
		if img.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
			image_files.remove(img)
		else:
			print(img)
			frames.append(imageio.imread("input/" + img))

	# Save them as frames into a gif 
	exportname = "output.gif"
	kargs = { 'duration': .05 }
	imageio.mimsave(exportname, frames, 'GIF', **kargs)


