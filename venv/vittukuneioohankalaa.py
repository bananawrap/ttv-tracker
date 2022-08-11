from PIL import ImageGrab, ImageChops
import time
img1 = ImageGrab.grab()
for i in range(3):
    time.sleep(1)
    print(i)
img2 = ImageGrab.grab()
img3 = ImageChops.blend(img1,img2,0.5)
img3.show()
