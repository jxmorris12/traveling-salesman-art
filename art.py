#
# jack morris 11/15/16
#

import tsp
import stipple as stippler
from PIL import Image

def __main__():
    #
    # print "__main__()"
    image_filename = "homer.jpg"
    #image_filename = "uva-logo.png"
    #image_filename = "smiley-grad.png"
    #image_filename = "cross.jpg"
    image = Image.open(image_filename).convert('L')
    stippled_image = stippler.stipple(image)
    tsp_image = tsp.connect_the_dots(stippled_image)
    tsp_image.show ()
    #

if __name__ == "__main__":
        __main__()
