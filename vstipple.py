#
# jack morris 11/08/16
#

from PIL import Image
import random
import math

#
# global variables
#
CENTROIDAL_DIFF_CONVERGENCE_LIMIT = 10**1
 
def voronoi_stipple(image):
  #image = Image.new("RGB", (width, height))
  pixels = image.load()
  putpixel = image.putpixel
  imgx, imgy = image.size
  #
  num_cells = (imgx + imgy)
  #
  print "Creating", num_cells,"stipples with convergence point", str(CENTROIDAL_DIFF_CONVERGENCE_LIMIT)+"."
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
  ccx = [[0] * imgx for y in range(imgy)]
  ccy = [[0] * imgx for y in range(imgy)]
  ccr = [[0] * imgx for y in range(imgy)]
  for y in range(imgy):
    for x in range(imgx):
      p = (1-pixels[x,y]/255.0) # rho
      ccr[y][x] = p
      ccx[y][x] = p*x
      ccy[y][x] = p*y
  # iterate
  while True:
    #
    #
    # shade regions and add up centroid totals
    new_cx = [0] * num_cells
    new_cy = [0] * num_cells
    new_ct = [0] * num_cells
    for y in range(imgy):
      for x in range(imgx):
        dmin = math.hypot(imgx-1, imgy-1)
        j = -1
        for i in range(num_cells):
          d = math.hypot(nx[i]-x, ny[i]-y)
          if d < dmin:
            dmin = d
            j = i
        new_cx[j] += ccx[y][x]
        new_cy[j] += ccy[y][x]
        new_ct[j] += ccr[y][x]
    # 
    #
    # compute new centroids
    centroidal_delta = 0
    for i in range(num_cells):
      new_cx[i] /= (new_ct[i] or 1)
      new_cy[i] /= (new_ct[i] or 1)
      centroidal_delta += math.hypot(new_cx[i]-nx[i],new_cy[i]-ny[i])
      nx[i] = new_cx[i]
      ny[i] = new_cy[i]
    # print difference
    print "Difference:", str(centroidal_delta) + "."
    # break if difference below convergence point
    if centroidal_delta < CENTROIDAL_DIFF_CONVERGENCE_LIMIT:
      break
  #
  #
  # mark final centroids on diagram
  for y in range(imgy):
    for x in range(imgx):
      putpixel((x, y), 0) # clear image for now
  for i in range(num_cells):
    pt = ( int(nx[i]), int(ny[i]))
    if pt == (0,0): 
      # SHOULD NOT HAPPEN
      continue
    putpixel(pt, 255)
  #
  return image
  #

def in_bounds(point, size):
    return (point[0] >= 0 and point[0] < size[0]) and (point[1] >= 0 and point[1] < size[1])

def cardinal_neighbors(pt):
    return [(pt[0]+1,pt[1]), (pt[0],pt[1]-1), (pt[0]-1,pt[1]),(pt[0],pt[1]+1)]