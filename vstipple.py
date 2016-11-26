#
# jack morris 11/08/16
#

from PIL import Image
import random
import math

#
# global variables
#
CENTROIDAL_DIFF_CONVERGENCE_LIMIT = 10
 
def voronoi_stipple(image):
  #image = Image.new("RGB", (width, height))
  pixels = image.load()
  putpixel = image.putpixel
  imgx, imgy = image.size
  #
  num_cells = (imgx + imgy) * 2
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
    centroidal_delta = 0
    for i in range(num_cells):
      i_start_pt = (int(nx[i]),int(ny[i]))
      q = [i_start_pt]
      cx = 0
      cy = 0
      ct = 0.0
      j = 0
      while j < len(q):
        pt = q[j]
        j += 1
        nn_x, nn_y = pt
        if region_data[pt] == region_data[i_start_pt]:
          # add to centroid
          cx += ccx[nn_y][nn_x]
          cy += ccy[nn_y][nn_x]
          ct += ccr[nn_y][nn_x]
          # BFS to continue queue
          for cn in cardinal_neighbors(pt):
            if in_bounds(cn, image.size) and cn not in q:
              q.append(cn)
      #
      #
      # reset d points
      new_cx = cx / (ct or 1)
      new_cy = cy / (ct or 1)
      centroidal_delta += (new_cx-nx[i])**2 + (new_cy-ny[i])**2
      nx[i] = new_cx
      ny[i] = new_cy
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