#
# jack morris 11/26/16
#

from PIL import Image, ImageDraw

# reads in an image composed of positive pixels (nodes) and negative pixels (free space)
# creates an approximate solution using a TSP heuristic
# outputs the image with the path traced out as one line

# store image pos and neg color
NEG_COLOR = None
POS_COLOR = None

#
# connect_the_dots (this file's main method)
#
def draw_dots_on(image):
    #
    nodes = read_in_nodes(image)
    print "Read in",len(nodes),"nodes."
    #
    return draw_dots(nodes, image)
    #

#
# draw a set of lines on an image
#
def draw_dots(nodes, image):
    #
    #
    # clear image
    imgx, imgy = image.size
    pixels = image.load()
    for y in xrange(imgy):
        for x in xrange(imgx):
            pixels[x,y] = NEG_COLOR
    #
    #
    # draw dots
    draw = ImageDraw.Draw(image)
    for node in nodes:
        draw_circle(draw, node, 2)
    #
    #
    # return
    return image
    #

#
#
# draws a circle with pillow ImageDraw
def draw_circle(image_draw, pt, radius):
    pt_1 = (pt[0]-radius,pt[1]-radius)
    pt_2 = (pt[0]+radius,pt[1]+radius)
    image_draw.ellipse([pt_1,pt_2], fill=POS_COLOR)
#
# read in nodes from input image
#
def read_in_nodes(image):
    #
    global NEG_COLOR,POS_COLOR
    #
    width, height = image.size
    pixels = image.load()
    nodes = []
    NEG_COLOR = pixels[0,0]
    print "Neg_color:", NEG_COLOR
    #
    for i in xrange(width):
        for j in xrange(height):
            #
            if pixels[i,j] != NEG_COLOR:
                #
                if not POS_COLOR:
                    POS_COLOR = pixels[i,j]
                #
                nodes.append( (i,j) )
                #
            #
        #
    #
    return nodes
    #
#