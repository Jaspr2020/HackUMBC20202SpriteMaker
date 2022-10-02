from PIL import Image, ImageDraw
im = Image.open("fantano.webp")

# The dimensions of the image that gets averaged
dimension = 1000

# Resizes image
im = im.resize((dimension, dimension), resample=0) 

# Makes array of tuples out of the image
pixels = im.load()
draw = ImageDraw.Draw(im)

# Gets user input 
size = int(input("Enter a sprite size: "))

jump = int(dimension/size)
ratio = int(dimension/jump)

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
# Shows image
im.show()

# Closes file
im.close()