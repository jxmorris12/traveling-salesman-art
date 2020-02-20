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
    folder_base = "output/"
    image_filename = "d-20161205180136" 
    image_extension = ".png"
    dotted_image = Image.open(folder_base + image_filename + image_extension).convert('L')
    #
    stippled_image = dot_stippler.draw_dots_on(dotted_image.copy(), True)
    stippled_image.show()
    stippled_image.save("output/s-" + image_filename + image_extension, "PNG")
    #
    # print ("Connecting image dots...")
    # tsp_image = tsp.connect_the_dots(dotted_image)
    # tsp_image.show()
    # export
    # tsp_image.save("output/t-" + image_filename + ".png", "PNG")
    #

if __name__ == "__main__":
        __main__()
