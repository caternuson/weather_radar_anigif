# Render supplied ani GIF as a matrix of circles to simulate an RGB LED matrix.

from PIL import Image, ImageDraw

# --| User Config |---------------------------------------------------
IMG_IN = "out.gif"
IMG_OUT = "matrix.gif"

NX = 64                 # number of circles in X
NY = 64                 # number of circles in Y
WX = 10                 # width of circle (pixels)
WY = 10                 # height of circle (pixels)
RR = 2                  # internal margin (pixels)
BG_COLOR = (0, 0, 0)    # fill color between circles
LOOP = 0                # 0=forever, N=number of loops
DURATION = 200          # ms per frame
# --| User Config |---------------------------------------------------

# input image
img_in = Image.open(IMG_IN)
DX = img_in.width / NX
DY = img_in.height / NY

# loop over frames
frames = []
FW = NX * WX
FH = NY * WY
for i in range(1, img_in.n_frames):

    # got to frame
    img_in.seek(i)

    # new output image frame and draw
    img_out = Image.new("RGBA", (FW, FH))
    img_draw = ImageDraw.Draw(img_out)
    img_draw.rectangle( (0, 0, FW, FH), fill=BG_COLOR)

    # sample loop
    sx = 0
    for xo in range(NX):
        sy = 0
        for yo in range(NY):
            # get "average color" from input image frame
            sample = img_in.crop( (sx, sy, sx+DX, sy+DY) )
            color = sample.resize( (1, 1), resample=Image.Resampling.BOX ).getpixel( (0, 0) )
            # compute bounding box for circle
            xx = xo * WX
            yy = yo * WY
            bb = (xx+RR, yy+RR, xx+WX-RR, yy+WY-RR)
            # draw circle
            img_draw.ellipse(bb , fill=color)

            sy += DY
        sx += DX

    # store frames
    frames.append(img_out)

# output ani gif
frames[0].save(
    IMG_OUT, save_all=True, append_images=frames, loop=LOOP, duration=DURATION
)
