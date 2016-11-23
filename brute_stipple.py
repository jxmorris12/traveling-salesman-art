#
# jack morris 11/08/16
#


from operator import itemgetter
from PIL import Image


#
def stipple(img):
  #
  width, height = img.size
  #
  MAX_STIPPLE_COUNT = (width * height) / 100 * 12
  DISTANCE_THRESHOLD = (width**2 + height**2) ** .5 / MAX_STIPPLE_COUNT * 32.0 # dumb, but this probably *SHOULD* reference the diagonal
  #
  pixels = img.load()
  #
  stipple_count = [ [0] * width for i in xrange(height) ]
  #
  max_counts = []
  #
  for i in xrange( 1, width-1 ):
    #
    for j in xrange( 1, height-1 ):
      #
      stipple_count[j][i] =  (pixels[i,j] - pixels[i-1,j])**2
      stipple_count[j][i] += (pixels[i,j] - pixels[i,j-1])**2 
      stipple_count[j][i] += (pixels[i,j] - pixels[i+1,j])**2
      stipple_count[j][i] += (pixels[i,j] - pixels[i,j+1])**2
      max_counts . append( [ stipple_count[j][i], (j,i) ] )
      #
    #
  #
  max_counts.sort(key=itemgetter(0)) # Sort by element 0 of tuple 
  max_counts = max_counts[-MAX_STIPPLE_COUNT:]
  #
  # normalize
  for i in xrange( width ):
      for j in xrange( height ):
          pixels[i,j] = 0
  # mark pixels
  marked_pixels = []
  #
  for x in xrange( len(max_counts) ):
    #
    i = max_counts[x][1][1]
    j = max_counts[x][1][0]
    #
    if min_distance_from_marked_pixels(marked_pixels, i, j) >= DISTANCE_THRESHOLD:
      # mark pixel as yes
      pixels[i,j] = 255
      marked_pixels.append((i,j))
      #
    #
  #
  # img.show()
  return img
  #
#
def min_distance_from_marked_pixels(marked_pixels, x, y):
  #
  min_distance = 100000000 # Dumb ... must be > img diagonal
  #
  for a in xrange(len(marked_pixels)):
    #
    i = marked_pixels[a][0]
    j = marked_pixels[a][1]
    #
    distance = ((x-i)**2 + (y-j)**2)**.5
    if distance < min_distance:
      #
      min_distance = distance
      #
  #
  return min_distance
  #
#
