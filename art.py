#
# jack morris 11/15/16
#

from PIL import Image
import vstipple as stippler
import greedy_tsp as tsp

def __main__():
    #
    # print "__main__()"
    #image_filename = "pics/homer.jpg"
    image_filename = "pics/uva-logo.png"
    #image_filename = "pics/smiley-grad.png"
    #image_filename = "pics/cross.jpg"
    image = Image.open(image_filename).convert('L')
    print "Stippling image..."
    stippled_image = stippler.voronoi_stipple(image)
    stippled_image.show()
    print "Connecting image dots..."
    tsp_image = tsp.connect_the_dots(stippled_image)
    tsp_image.show()
    # export
    tsp_image.save("tsp.png", "PNG")
    #

if __name__ == "__main__":
        __main__()
