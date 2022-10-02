from PIL import Image, ImageDraw
im = Image.open("fantano.webp")
dimension = 1000

 
im = im.resize((dimension, dimension), resample=0) 
pixels = im.load()
draw = ImageDraw.Draw(im)
size = int(input("Enter a sprite size: "))

jump = int(dimension/size)
ratio = int(dimension/jump)
for i in range(ratio):
    #print(i)
    for j in range(ratio):
        rsum = 0
        gsum = 0
        bsum = 0
        for k in range(jump):
            for l in range(jump):
           
                rsum += pixels[(i * jump) + k,(j * jump) + l][0]
                gsum += pixels[(i * jump) + k,(j * jump) + l][1]
                bsum += pixels[(i * jump) + k,(j * jump) + l][2]

    

        fill =(round(rsum/(jump * jump)), round(gsum/(jump * jump)), round(bsum/(jump * jump)))
        draw.rectangle((i * jump, j * jump, (i * jump) + jump, (j * jump) + jump), fill, outline=None)
im.show()

im.close()