#
# jack morris 11/08/16
#

from PIL import Image
import random
import math
 
def generate_voronoi_diagram(num_cells):
  image = Image.open("pics/uva-logo.png").convert("L") 
  #image = Image.new("RGB", (width, height))
  pixels = image.load()
  putpixel = image.putpixel
  imgx, imgy = image.size
  #
  nx = []
  ny = []
  nr = []
  #
  region_data = {}
  # random seed points
  for i in range(num_cells):
    nx.append(random.randrange(imgx))
    ny.append(random.randrange(imgy))
    nr.append(random.randrange(256))
  # compute centroids
  for y in range(imgy):
    for x in range(imgx):
      dmin = math.hypot(imgx-1, imgy-1) * 1
      j = -1
      for i in range(num_cells):
          d = math.hypot(nx[i]-x, ny[i]-y) * (1-pixels[x,y]/255.)
          if d < dmin:
            dmin = d
            j = i
      region_data[x,y] = j
      putpixel((x, y), 0) # clear image for now
  # find centroids
  centroids = []
  print "0.0%"
  for i in range(num_cells):
    print str((i+1)*1.0/num_cells*100)+"%"
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
        cx += nn_x * 1 # rho = 1 for now
        cy += nn_y * 1 # " 
        ct += 1
        # BFS to continue queue
        for cn in cardinal_neighbors(pt):
            if in_bounds(cn, image.size) and cn not in q:
                q.append(cn)
    if ct == 0: 
     continue
    cx /= ct
    cy /= ct
    centroids += [(int(cx), int(cy))]
  # mark centroids
  print "Number of cells:", num_cells, "Number of centroids:", len(centroids)
  for c in centroids:
    print "Putting pixel at centroid:", c
    putpixel(c, 255)
  # save
  image.save("VoronoiDiagram.png", "PNG")
  image.show()

def in_bounds(point, size):
    return (point[0] >= 0 and point[0] < size[0]) and (point[1] >= 0 and point[1] < size[1])

def cardinal_neighbors(pt):
    return [(pt[0]+1,pt[1]), (pt[0],pt[1]-1), (pt[0]-1,pt[1]),(pt[0],pt[1]+1)]

generate_voronoi_diagram(50)
