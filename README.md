Code for generating a synthetic dataset for image captioning. The data produced for each data element are:
-an image of shapes (circles and rectangles) of different colours recursively containing other figures.
-a XML tree describing the hierarchy of the shapes composing the image (maximum depth is 3).
- a sentence (English language) describing the image with different levels of detail: figures in the first two levels of the hierarchy are listed using their shape and colour, figures in the third level are described only with their number.

This dataset has different purposes: as long as the standard image captioning task, it is possible to tackle this problem as a trees transduction task. 
Indeed it is possible to get input trees labelled with CNN information from images and XML trees.
XML trees can also be used as targets thus defining isomorphic tree transduction.
Finally, the sentences can be processed with suitable software to get parse trees or dependency trees. Using these trees as targets we define a non-isomorphic tree transduction problem.
