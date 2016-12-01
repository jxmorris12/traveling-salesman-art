#
# jack morris 11/15/16
#

import dot_stippler
import greedy_tsp as tsp
from PIL import Image
from time import gmtime, strftime
import vstipple as stippler

def __main__():
    #
    image_filename = "input/pikachu.png" 
    image = Image.open(image_filename).convert('L')
    #
    showtime = strftime("%Y%m%d%H%M%S", gmtime())
    #
    dotted_image = stippler.voronoi_stipple(image)
    dotted_image.show()
    dotted_image.save("output/d-" + showtime + ".png", "PNG")
    #
    # stippled_image = dot_stippler.draw_dots_on(dotted_image.copy())
    # stippled_image.show()
    # stippled_image.save("output/s-" + showtime + ".png", "PNG")
    #
    print "Connecting image dots..."
    tsp_image = tsp.connect_the_dots(dotted_image)
    tsp_image.show()
    # export
    tsp_image.save("output/t-" + showtime + ".png", "PNG")
    #

if __name__ == "__main__":
        __main__()
