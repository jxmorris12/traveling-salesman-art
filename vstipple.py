#
# jack morris 11/08/16
#

import math
import numpy as np
from PIL import Image
import random
from time import gmtime, strftime

#
# global variables
#
NEG_COLOR = 255
POS_COLOR = 0
CONVERGENCE_LIMIT = 10**-4
DEFAULT_RESOLUTION = 1
 
def voronoi_stipple(image):
  #image = Image.new("RGB", (width, height))
  pixels = image.load()
  putpixel = image.putpixel
  imgx, imgy = image.size
  #
  num_cells = (imgx + imgy) * 2
  #
  showtime = strftime("%Y%m%d%H%M%S", gmtime())
  print "(+) Creating", num_cells,"stipples with convergence point", str(CONVERGENCE_LIMIT)+"."
  #
  nx = []
  ny = []
  #
  region_data = {}
  # 
  #
  # random seed points
  for i in range(num_cells):
    nx.append(random.randrange(imgx))
    ny.append(random.randrange(imgy))
  #
  #
  # precompute centroid data
  rho = [[0] * imgx for y in range(imgy)]
  #
  for y in range(imgy):
    for x in range(imgx):
      rho[y][x] = 1 - pixels[x,y]/255.0 # rho
  #
  clear_image(image.size, putpixel)
  draw_points(zip(nx,ny), putpixel, image.size)
  image.save("output/_step/" + showtime + "-" + str(0) + ".png", "PNG")
  # iterate
  new_cx = [0] * num_cells
  new_cy = [0] * num_cells
  new_ct = [0] * num_cells
  iteration = 1
  resolution = DEFAULT_RESOLUTION
  max_hypot = imgx**2 + imgy**2
  while True:
    zero_list( new_cx )
    zero_list( new_cy )
    zero_list( new_ct )
    #
    #
    # shade regions and add up centroid totals
    res_step = 1.0 / (resolution)
    for y_step in np.arange(res_step/2.0, imgy, res_step):
      y = int( y_step )
      for x_step in np.arange(res_step/2.0, imgx, res_step):
        x = int( x_step )
        d_min = max_hypot
        i_min = None
        for i in range(num_cells):
          d = math.hypot(nx[i]-x_step, ny[i]-y_step)
          if d < d_min:
            d_min = d
            i_min = i
        r = rho[y][x]
        new_cx[i_min] += r * x_step
        new_cy[i_min] += r * y_step
        new_ct[i_min] += r
    # 
    #
    # compute new centroids
    centroidal_delta = 0
    i = 0
    while i < num_cells:
      if not new_ct[i]:
        # all pixels in region have rho = 0
        # remove centroid
        del new_cx[i]
        del new_cy[i]
        del new_ct[i]
        del nx[i]
        del ny[i]
        num_cells -= 1
      else:
        new_cx[i] /= new_ct[i]
        new_cy[i] /= new_ct[i]
        # print "centroidal_delta", centroidal_delta
        centroidal_delta += hypot_square( (new_cx[i]-nx[i]), (new_cy[i]-ny[i]) )
        nx[i] = new_cx[i]
        ny[i] = new_cy[i]
        i += 1
    # print difference
    print "Difference:", str(centroidal_delta) + "."
    # save a copy of the image (to GIF later)
    clear_image(image.size, putpixel)
    draw_points(zip(nx,ny), putpixel, image.size)
    image.save("output/_step/" + showtime + "-" + str(iteration) + ".png", "PNG")
    iteration += 1
    # break if difference below convergence point
    if centroidal_delta == 0.0:
      resolution *= 2
      print "(+) Increasing resolution to " + str(resolution) + "x."
    elif centroidal_delta < CONVERGENCE_LIMIT:
      break
  #
  clear_image(image.size, putpixel)
  draw_points(zip(nx,ny), putpixel, image.size)
  #
  return image
  #

def zero_list(the_list):
  for x in xrange( len(the_list) ):
    the_list[x] = ld(0)

def clear_image(size, putpixel):
  #
  imgx, imgy = size
  for y in range(imgy):
    for x in range(imgx):
      putpixel((x, y), NEG_COLOR) # clear image for now
  #

def draw_points(points, putpixel, size):
  #
  for i in range(len(points)):
    pt = round_point( points[i] )
    if pt == (0,0): 
      # Skip pixels at origin - they'll mess up the stippler
      continue
    putpixel(pt, POS_COLOR)
  #

def round_point(pt):
  return ( int(round(pt[0])), int(round(pt[1])) )

def ld(x):
  return np.longdouble(x)

def hypot_square( d1, d2 ):
  return d1**2 + d2**2