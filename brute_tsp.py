#
# jack morris 11/15/16
#

from PIL import Image, ImageDraw

# reads in an image composed of positive pixels (nodes) and negative pixels (free space)
# creates an approximate solution using a TSP heuristic
# outputs the image with the path traced out as one line


# uses a version of the nearest-neighbor approximation as follows:
# take a random node
# choose the nearest neighbor to that node that has not been chosen

# store image pos and neg color
NEG_COLOR = None
POS_COLOR = None

#
# connect_the_dots (this file's main method)
#
def connect_the_dots(image):
    #
    nodes = read_in_nodes(image)
    print "Read in",len(nodes),"nodes."
    #
    lines = connect_dots_with_lines(read_in_nodes(image))
    print "Calculated nearest neighbors."
    #
    return draw_lines_on_image(lines, image)
    #

#
# draw a set of lines on an image
#
def draw_lines_on_image(lines, image):
    #
    draw = ImageDraw.Draw(image)
    #
    for line in lines:
        #
        point1 = line[0]
        point2 = line[1]
        #
        points = (point1, point2)
        #
        draw.line( points, fill=POS_COLOR )
        #
    # free up some space
    del draw
    #
    return image


#
# connect a set of nodes with one continguous line
#
def connect_dots_with_lines(dots):
    #
    lines = []
    #
    next_dot = dots.pop()
    #
    while dots:
        # @TODO: check for overlapping lines
        min_distance = 1000000
        closest_dot = None
        for dot in dots:
            #
            distance = (dot[0]-next_dot[0])**2 + (dot[1]-next_dot[1])**2
            #
            if distance < min_distance:
                #
                closest_dot = dot
                min_distance = distance
                #
            #
        #
        if closest_dot:
            lines.append( ( next_dot, closest_dot ) )
        #
        dots.remove(closest_dot)
        next_dot = closest_dot
        #
    #
    return lines
    #

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