#
# jack morris 11/21/16
#

from PIL import Image, ImageDraw
from tsp_solver.greedy import solve_tsp

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
    #
    # build upper triangular distance matrix between dots
    distance_matrix = [[0] * len(dots) for x in range(len(dots))]
    for i in range(len(dots)):
        for j in range(i+1,len(dots)):
            d = distance_between(dots[i], dots[j])
            distance_matrix[i][j] = d
            distance_matrix[j][i] = d
    #
    #
    # ask for TSP solution
    path = solve_tsp( distance_matrix )
    #
    #
    # create lines
    last_node = dots[path[0]]
    for x in range(1,len(path)):
        next_node = dots[path[x]]
        lines.append( (last_node, next_node) )
        last_node = next_node
    #
    return lines
    #

#
# find the distance between two tuples
#
def distance_between(d1, d2):
    return (d1[0] - d2[0])**2 + (d1[1] - d2[1])**2

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