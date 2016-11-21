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
# if this line overlaps any lines drawn previously, pick the next-nearest node and check again
# if no nodes are left to connect without drawing overlapping lines, skip this node

# global settings
DRAW_ARC = False

# store image pos and neg color
NEG_COLOR = None
POS_COLOR = None

#
# connect_the_dots (this file's main method)
#
def connect_the_dots(image):
    #
    nodes = read_in_nodes(image)
    #
    lines = connect_dots_with_lines(read_in_nodes(image))
    #
    return draw_lines(lines, image)
    #

#
# draw a set of lines on an image
#
def draw_lines(lines, image):
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
        if DRAW_ARC:
            draw.arc( points, 0, 90, fill=POS_COLOR ) 
        else:
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
    while dots:
        next_dot = dots.pop()
        # @TODO: check for overlapping lines
        min_distance = 1000000
        closest_dot = None
        for dot in dots:
            #
            distance = (dot[0]-next_dot[0])**2 + (dot[1]-next_dot[1])**2
            #
            if distance < min_distance:# and no_line_overlap( (next_dot,dot), lines):
                #
                closest_dot = dot
                min_distance = distance
                #
            #
        #
        if closest_dot:
            lines.append( ( next_dot, closest_dot ) )
    #
    return lines
    #
#
# determine if [new_line] would cross any lines defined in [lines]
#
def no_line_overlap(new_line, lines):
    #
    p0 = new_line[0]
    p1 = new_line[1]
    #
    for old_line in lines:
        #
        p2 = old_line[0]
        p3 = old_line[1]
        #
        if find_intersection(p0,p1,p2,p3) is not None: return False
        #
    #
    return True
    #
#


def find_intersection( p0, p1, p2, p3 ) :
    # line segment intersection code from StackOverflow /u/Kris
    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]
    denom = s10_x * s32_y - s32_x * s10_y
    if denom == 0 : return None # collinear
    denom_is_positive = denom > 0
    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]
    s_numer = s10_x * s02_y - s10_y * s02_x
    if (s_numer < 0) == denom_is_positive : return None # no collision
    t_numer = s32_x * s02_y - s32_y * s02_x
    if (t_numer < 0) == denom_is_positive : return None # no collision
    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision
    # collision detected
    t = t_numer / denom
    intersection_point = [ p0[0] + (t * s10_x), p0[1] + (t * s10_y) ]
    return intersection_point#

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
