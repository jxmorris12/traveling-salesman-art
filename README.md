# traveling-salesman-art

This is my implementation of creating Traveling Salesman Artwork with Weighted Voronoi Stipplings. Check out the writeup on my website [here](http://jackxmorris.com/posts/traveling-salesman-art).

Here's what the files do:

`art.py` is the main file to run. It loads an image, stipples it, adjusts the stippling, and then finds a nearest-neighbor TSP solution to the system. It outputs to an `output/` folder.
`vstippler.py` takes an image and generates a Weighted Voronoi Stippling for it.
`dot_stippler.py` takes the dotted version of an image and tidies it up - magnifies it and replaces the single-pixel dots with larger circles for nicer effect.
`greedy_tsp.py` takes the image of dots and connects them all via a Traveling Salesman Approximation.
