#
# jack morris 11/08/16
#

from PIL import Image
import random
import math
 
def voronoi_stipple(image):
  #image = Image.new("RGB", (width, height))
  pixels = image.load()
  putpixel = image.putpixel
  imgx, imgy = image.size
  #
  num_cells = (imgx + imgy) / 4
  iter_limit = num_cells / 20
  #
  print "Creating", num_cells,"stipples via",iter_limit,"iterations."
  print
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
  # iterate
  for iterator in range(iter_limit):
    print "Iteration",iterator+1,"of",str(iter_limit)+"."
    #
    #
    # shade regions
    for y in range(imgy):
      for x in range(imgx):
        dmin = math.hypot(imgx-1, imgy-1)
        j = -1
        for i in range(num_cells):
          d = math.hypot(nx[i]-x, ny[i]-y)
          if d < dmin:
            dmin = d
            j = i
        region_data[x,y] = j
    #
    #
    # compute centroids
    for i in range(num_cells):
      start_pt = (nx[i],ny[i])
      q = [start_pt]
      cx = 0
      cy = 0
      ct = 0.0
      j = 0
      while j < len(q):
        pt = q[j]
        j += 1
        nn_x, nn_y = pt
        if region_data[pt] == region_data[start_pt]:
          # add to centroid
          rho = (1-pixels[pt]/255.0)
          cx += nn_x * rho # rho = 1 for now
          cy += nn_y * rho # " 
          ct += rho
          # BFS to continue queue
          for cn in cardinal_neighbors(pt):
            if in_bounds(cn, image.size) and cn not in q:
              q.append(cn)
      #
      #
      # reset d points
      nx[i] = int( cx/(ct or 1) )
      ny[i] = int( cy/(ct or 1) )
  #
  #
  # mark final centroids on diagram
  for y in range(imgy):
    for x in range(imgx):
      putpixel((x, y), 0) # clear image for now
  for i in range(num_cells):
    pt = (nx[i], ny[i])
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