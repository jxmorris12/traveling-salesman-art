#
# jack morris 11/08/16
#

import itertools
import math
import numpy as np
import os
from PIL import Image
import random
from scipy import spatial
import sys
from time import gmtime, strftime

#
# global variables
#
NEG_COLOR = 255
POS_COLOR = 0
CONVERGENCE_LIMIT = 5 * 10**-4
DEFAULT_RESOLUTION = 1
FINAL_MAGNIFICATION = 8
 
def voronoi_stipple(image):
  #
  pixels = image.load()
  putpixel = image.putpixel
  imgx, imgy = image.size
  #
  num_cells = (imgx + imgy) * 8
  #
  showtime = strftime("%Y%m%d%H%M%S", gmtime())
  print "(+) Creating", num_cells,"stipples with convergence point", str(CONVERGENCE_LIMIT)+"."
  #
  centroids = [
    [random.randrange(imgx) for x in xrange(num_cells)],
    [random.randrange(imgy) for x in xrange(num_cells)]
  ]
  # 
  #
  # precompute pixel densities
  rho = [[0] * imgx for y in range(imgy)]
  for y in range(imgy):
    for x in range(imgx):
      rho[y][x] = 0 + pixels[x,y]/255.0 # rho
  #
  #
  # make folder to save each snapshot
  folder_base = "output/_step/" + showtime + "/"
  os.makedirs(folder_base)
  #
  #
  # save initial image
  clear_image(image.size, putpixel)
  draw_points(zip_points(centroids), putpixel, image.size)
  image.save(folder_base + "0.png", "PNG")
  #
  #
  # empty arrays for storing new centroid sums
  new_centroid_sums = [
    [0] * num_cells,  # x component
    [0] * num_cells,  # y component
    [0] * num_cells   # density
  ]
  # 
  #
  # Iterate
  iteration = 1
  resolution = DEFAULT_RESOLUTION
  while True:
    zero_list( new_centroid_sums[0] )
    zero_list( new_centroid_sums[1] )
    zero_list( new_centroid_sums[2] )
    #
    # shade regions and add up centroid totals
    sum_regions(centroids, new_centroid_sums, rho, 1.0 / resolution, image.size)
    # compute new centroids
    centroidal_delta = compute_centroids(len(centroids[0]), centroids, new_centroid_sums)
    # print difference
    printr( str(iteration) + "     \tDifference: " + str(centroidal_delta) + ".\n" )
    # save a copy of the image (to GIF later)
    clear_image(image.size, putpixel)
    draw_points(zip_points(centroids), putpixel, image.size)
    image.save(folder_base + str(iteration) + ".png", "PNG")
    iteration += 1
    # break if difference below convergence point
    if centroidal_delta == 0.0:
      resolution *= 2
      print "(+) Increasing resolution to " + str(resolution) + "x."
    elif centroidal_delta < CONVERGENCE_LIMIT:
      break
  #
  print "(+) Magnifying image and drawing final centroids."
  #
  return magnify_and_draw_points(zip_points(centroids), image.size)
  #

def compute_centroids(num_cells, centroids, new_centroid_sums):
  centroidal_delta = 0
  i = 0
  while i < num_cells:
    if not new_centroid_sums[2][i]:
      # all pixels in region have rho = 0
      # remove centroid
      del new_centroid_sums[0][i]
      del new_centroid_sums[1][i]
      del new_centroid_sums[2][i]
      del centroids[0][i]
      del centroids[1][i]
      num_cells -= 1
    else:
      new_centroid_sums[0][i] /= new_centroid_sums[2][i]
      new_centroid_sums[1][i] /= new_centroid_sums[2][i]
      # print "centroidal_delta", centroidal_delta
      centroidal_delta += hypot_square( (new_centroid_sums[0][i]-centroids[0][i]), (new_centroid_sums[1][i]-centroids[1][i]) )
      centroids[0][i] = new_centroid_sums[0][i]
      centroids[1][i] = new_centroid_sums[1][i]
      i += 1
  return centroidal_delta

def sum_regions(centroids, new_centroid_sums, rho, res_step, size):
  #
  #
  # construct 2-dimensional tree from generating points
  tree = spatial.KDTree(zip(centroids[0], centroids[1]))
  #
  imgx, imgy = size
  x_range = np.arange(res_step/2.0, imgx, res_step)
  y_range = np.arange(res_step/2.0, imgy, res_step)
  point_matrix = list(itertools.product(x_range, y_range))
  nearest_nbr_indices = tree.query(point_matrix)[1]
  for i in xrange(len(point_matrix)):
    point = point_matrix[i]
    x = point[0]
    y = point[1]
    r = rho[int(y)][int(x)]
    nearest_nbr_index = nearest_nbr_indices[i]
    new_centroid_sums[0][nearest_nbr_index] += r * x
    new_centroid_sums[1][nearest_nbr_index] += r * y
    new_centroid_sums[2][nearest_nbr_index] += r
    #
    if i % 10 == 0:
      #
      perc = float(i) / len(point_matrix)
      printr( "{:.2%}".format(perc) )
      #
    #
  #

def zip_points(p):
  return zip(p[0], p[1])

def printr(s):
  sys.stdout.write( "\r" + s )
  sys.stdout.flush()

def zero_list(the_list):
  for x in xrange( len(the_list) ):
    the_list[x] = 0

def clear_image(size, putpixel):
  #
  imgx, imgy = size
  for y in range(imgy):
    for x in range(imgx):
      putpixel((x, y), NEG_COLOR) # clear image for now
  #

def magnify_and_draw_points(points, size):
  #
  magnified_size = (size[0] * FINAL_MAGNIFICATION, size[1] * FINAL_MAGNIFICATION)
  blank_magnified_image = Image.new("L", magnified_size)
  putpixel = blank_magnified_image.putpixel
  clear_image(magnified_size, putpixel)
  #
  #
  magnified_points = [tuple(FINAL_MAGNIFICATION*x for x in point) for point in points]
  #
  draw_points(magnified_points, putpixel, magnified_size)
  #
  return blank_magnified_image
  #

def draw_points(points, putpixel, size):
  #
  for i in range(len(points)):
    pt = round_point( points[i] )
    if pt == (0,0): 
      # Skip pixels at origin - they'll break the TSP art
      continue
    putpixel(pt, POS_COLOR)
  #

def round_point(pt):
  return ( int(pt[0]), int(pt[1]) )

def hypot_square( d1, d2 ):
  if d1 == 0 and d2 == 0: return 0
  elif d1 == 0: return d2 ** 2
  elif d2 == 0: return d1 ** 2
  return d1**2 + d2**2