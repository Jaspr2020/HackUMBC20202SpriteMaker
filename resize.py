from PIL import Image, ImageDraw
im = Image.open("Ninja.jpg")
im = im.resize((1024, 1024), resample=0) 
pixels = im.load()
draw = ImageDraw.Draw(im)

ratio = 64
jump = int(ratio/4)
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
        fill =(int(rsum/256), int(gsum/256), int(bsum/256))
        draw.rectangle((i * jump, j * jump, (i * jump) + jump, (j * jump) + jump), fill, outline=None)
im.show()

im.close()