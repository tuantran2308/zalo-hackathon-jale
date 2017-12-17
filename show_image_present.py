import matplotlib.pyplot as plt
import time
from utils import FileTool

img_next=plt.imread('next.png')
img_prev=plt.imread('prev.png')
img_punch=plt.imread('punch.png')
img_hook=plt.imread('hook.png')
img_lock=plt.imread('lock.png')
img_unlock=plt.imread('unlock.png')
img_blank=plt.imread('exercise.png')


list = [img_lock, img_punch, img_unlock, img_hook, img_next, img_prev, img_blank]
old_index = -1 
img =None
# while True:
print 'before'
ind = 6
while True:
	try:
		ind = FileTool.readPickle("index_img")
	except:
		ind = -1
	f = list[ind]
	if img is None:
	   	img = plt.imshow(f)	
	else:
	   	img.set_data(f)

	plt.pause(0.2)
	plt.draw()