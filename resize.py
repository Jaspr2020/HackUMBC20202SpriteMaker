from PIL import Image, ImageDraw
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation 

segmentor = SelfiSegmentation()

# Get name of file from user
filename = input("What is the name of your file? (must me in project directory): ")

#Open the file as an image using PIL
im = Image.open(filename)

# Gets user input of whether to remove the background of the image or not
remove_bg = ""
while remove_bg != "yes" and remove_bg != "no":
    remove_bg = input("Remove background? (yes/no)")
# Gets user input to determine which pizelerization method to be used
size_or_scale = ""
while size_or_scale != "size" and size_or_scale != "scale":
    size_or_scale = input("size or scale: ")

# Store the size of the image as the dimension
dimension = im.size
# If the imaeg will be resized set the dimension to 1000, 1000
if size_or_scale == "size":
    # The dimensions of the image that gets averaged
    dimension = (int(1000), int(1000))
    # Resizes image
    im = im.resize(dimension, resample=0) 

# Read in the image
img = cv2.imread(filename)

# If the user want's the background removed
if remove_bg == "yes":
    # Remove background
    img = segmentor.removeBG(img, (255, 255, 255), threshold=0.4)
    cv2.imwrite("noBack.jpg", img)
    im = Image.open("noBack.jpg")
    img = cv2.imread("noBack.jpg")

# Outline algorithm
gray_Img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
orig_blur = cv2.GaussianBlur(gray_Img, (21, 21), 0)
sketchy = cv2.divide(gray_Img, orig_blur, scale = 256.0)
cv2.imwrite("pencil.jpg", sketchy)

# Open the images as PIL images
im2 = Image.open("pencil.jpg")
im2 = im2.resize((dimension[0], dimension[1]), resample=0) 

# Get pixels from both images 
# Makes array of tuples out of the image
pixels = im.load()
pixels2 = im2.load()
draw = ImageDraw.Draw(im)

# Get scaling factor 
if size_or_scale == "size":
    # Gets user input
    s = int(input("Enter a sprite size: "))
    scale_factor = dimension[0] / s
elif size_or_scale == "scale":
    scale_factor = int(input("Enter a scaling factor: "))

# The size of the pizelerized image
size = (int(dimension[0] / scale_factor), int(dimension[1] / scale_factor))
# The amount of mixels to jump for the pixelerized image
jump = (int(dimension[0] / size[0]), int(dimension[1] / size[1]))
ratio = (int(dimension[0] / jump[0]), int(dimension[1] / jump[1]))
for i in range(ratio[0]):
    for j in range(ratio[1]):
        for k in range(jump[0]):
            for l in range(jump[1]):
                sum = pixels[(i * jump[0]) + k,(j * jump[1]) + l][0] + pixels[(i * jump[0]) + k,(j * jump[1]) + l][1] + pixels[(i * jump[0]) + k,(j * jump[1]) + l][2]
                if sum < 100:
                    pixels[(i * jump[0]) + k,(j * jump[1]) + l] = (0, 0, 0)

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

# Ask whether or not to save the image
save = ""
while save != "yes" and save != "no":
    save = input("Save? (yes/no): ")
# Save the image with info about it
if save == "yes":
    extra = ""
    if size_or_scale == "size":
        extra = str(size) + "x" + str(size)
    elif size_or_scale == "scale":
        extra = str(scale_factor)
    im.save(filename+extra+".jpg")

# Closes file
im.close()