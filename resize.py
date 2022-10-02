from hashlib import new
from PIL import Image, ImageDraw
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation 

segmentor = SelfiSegmentation()

filename = "Dog.png"
im = Image.open(filename)

# Gets user input pip
size_or_scale = input("Size or Scale: ")

dimension = im.size

if size_or_scale == "size":
    # The dimensions of the image that gets averaged
    dimension = 1000
    # Resizes image
    im = im.resize((dimension, dimension), resample=0) 
elif size_or_scale == "scale":
    dimension = im.size

# read in image
img = cv2.imread(filename)

img = segmentor.removeBG(img, (255, 255, 255), threshold=0.4)
cv2.imwrite("noBack.jpg", img)

noBackIm = Image.open("noBack.jpg")

img = cv2.imread("noBack.jpg")
# convert to grayscale
gray_Img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# blur
orig_blur = cv2.GaussianBlur(gray_Img, (21, 21), 0)

# Create pencil sketch
sketchy = cv2.divide(gray_Img, orig_blur, scale = 256.0)
cv2.imwrite("pencil.jpg", sketchy)

im2 = Image.open("pencil.jpg")

if size_or_scale == "size":
    im2 = im2.resize((dimension, dimension), resample=0) 

#im2.show()
#cv2.wait(0)
# Makes array of tuples out of the image
pixels = noBackIm.load()


pixels2 = im2.load()

draw = ImageDraw.Draw(im)

if size_or_scale == "size":
    # Gets user input
    size = int(input("Enter a sprite size: "))
    jump = int(dimension/size)
    ratio = int(dimension/jump)
    for i in range(ratio):
        for j in range(ratio):
            for k in range(jump):
                for l in range(jump):
                    sum = pixels[(i * jump) + k,(j * jump) + l][0] + pixels[(i * jump) + k,(j * jump) + l][1] + pixels[(i * jump) + k,(j * jump) + l][2]
                    if sum < 50 * 3:
                        pixels[(i * jump) + k,(j * jump) + l] = (0, 0, 0)
elif size_or_scale == "scale":
    scale_factor = int(input("Enter a scaling factor: "))
    size = (int(dimension[0] / scale_factor), int(dimension[1] / scale_factor))
    jump = (int(dimension[0] / size[0]), int(dimension[1] / size[1]))
    ratio = (int(dimension[0] / jump[0]), int(dimension[1] / jump[1]))
    for i in range(ratio[0]):
        for j in range(ratio[1]):
            for k in range(jump[0]):
                for l in range(jump[1]):
                    sum = pixels[(i * jump[0]) + k,(j * jump[1]) + l][0] + pixels[(i * jump[0]) + k,(j * jump[1]) + l][1] + pixels[(i * jump[0]) + k,(j * jump[1]) + l][2]
                    if sum < 50 * 3:
                        pixels[(i * jump[0]) + k,(j * jump[1]) + l] = (0, 0, 0)


if size_or_scale == "size":
    # Loops for each row of squares
    for i in range(ratio):
        # Loops for each column 
        for j in range(ratio):
            # sets red, green and blue sums to 0
            rsum = 0
            gsum = 0
            bsum = 0

            # Sums pixel values out in square of size jump by jump
            for k in range(jump):
                for l in range(jump):

                    rsum += pixels[(i * jump) + k,(j * jump) + l][0]
                    gsum += pixels[(i * jump) + k,(j * jump) + l][1]
                    bsum += pixels[(i * jump) + k,(j * jump) + l][2]

        
            # Sets color of square to average of pixels
            fill =(round(rsum/(jump * jump)), round(gsum/(jump * jump)), round(bsum/(jump * jump)))
            
            # Draws square
            draw.rectangle((i * jump, j * jump, (i * jump) + jump, (j * jump) + jump), fill, outline=None)

if size_or_scale == "scale":
    # Loops for each row of squares
    for i in range(ratio[0]):
        # Loops for each column 
        for j in range(ratio[1]):
            # sets red, green and blue sums to 0
            rsum = 0
            gsum = 0
            bsum = 0

            # Sums pixel values out in square of size jump by jump
            for k in range(jump[0]):
                for l in range(jump[1]):

                    rsum += pixels[(i * jump[0]) + k,(j * jump[1]) + l][0]
                    gsum += pixels[(i * jump[0]) + k,(j * jump[1]) + l][1]
                    bsum += pixels[(i * jump[1]) + k,(j * jump[1]) + l][2]

        
            # Sets color of square to average of pixels
            fill =(round(rsum/(jump[0] * jump[1])), round(gsum/(jump[0] * jump[1])), round(bsum/(jump[0] * jump[1])))
            
            # Draws square
            draw.rectangle((i * jump[0], j * jump[1], (i * jump[0]) + jump[0], (j * jump[1]) + jump[1]), fill, outline=None)
    
# Shows image
im.show()

# Closes file
im.close()