#
# jack morris 11/15/16
#

import greedy_tsp as tsp
from PIL import Image
from time import gmtime, strftime
import vstipple as stippler

def __main__():
    #
    image_filename = "pics/smiley-grad.png" #-small.png"
    image = Image.open(image_filename).convert('L')
    #
    showtime = strftime("%Y%m%d%H%M%S", gmtime())
    #
    stippled_image = stippler.voronoi_stipple(image)
    stippled_image.show()
    stippled_image.save("output/s-" + showtime + ".png", "PNG")
    #
    print "Connecting image dots..."
    tsp_image = tsp.connect_the_dots(stippled_image)
    tsp_image.show()
    # export
    tsp_image.save("output/t-" + showtime + ".png", "PNG")
    #

if __name__ == "__main__":
        __main__()
