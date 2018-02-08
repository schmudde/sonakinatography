import svgwrite

############## Setup

def write_svg(svg, path):
  with open(path, "w") as f:
    f.write(svg.tostring())
  return {'kind': 'file', 'content_type': 'image/svg+xml', 'coder': 'svg'}

dwg = svgwrite.Drawing('test.svg', profile='tiny')

yellow_green=svgwrite.rgb(0, 204, 0)   # Yellow Green
green=svgwrite.rgb(0, 102, 0)          # Green
blue=svgwrite.rgb(0, 0, 255)           # Blue
blue_violet=svgwrite.rgb(127, 0, 255)  # Blue Violet
red_violet=svgwrite.rgb(153, 0, 153)   # Red Violet
red=svgwrite.rgb(204, 0, 0)            # Red
orange=svgwrite.rgb(255, 128, 0)       # Orange
yellow=svgwrite.rgb(255, 255, 0)       # Yellow

color_grid = [yellow_green, green, blue, blue_violet, red_violet, red, orange, yellow]

# Painter

square_size = 20          # TODO: Redundant with Utils
def scale_square(x, y):   # TODO: Redundant with Utils (modified)
  return ((x*square_size), (y*square_size))

def print_square(square):
  print square['size'],

def print_line():
  print "|",

# TODO: def paint_line():
#

def paint_square(square, beat, max_beat):
  color = (square['size'] - 1)
  x, y = scale_square(square['lane'], beat)
  y = abs(y - (max_beat * square_size))
  dwg.add(dwg.rect((x, y), (square_size,square_size), fill=color_grid[color]))

# Builder

def reset_square(square):
  if square['size'] == 1:
    square['size'] = 8
  else:
    square['size'] -= 1
  square['countdown'] = square['size']
  return square

def build_row(squ_matrix, beat, max_beat):
  for square in squ_matrix:
    square['countdown'] -= 1
    if square['countdown'] == 0:
      #print_square(square)
      paint_square(square, beat, max_beat)
      square = reset_square(square)
    else:
      print_line()
  return squ_matrix

def build_columns(squ_matrix, max_beat):
  beat = 0
  while beat < max_beat:
    beat += 1
    squ_matrix = build_row(squ_matrix, beat, max_beat)
    print(" ")

def matrix_traverser(max_beat):
  squ_matrix = [{'size': 1, 'countdown': 1, 'lane': 0},
                {'size': 2, 'countdown': 2, 'lane': 1},
                {'size': 3, 'countdown': 3, 'lane': 2},
                {'size': 4, 'countdown': 4, 'lane': 3},
                {'size': 5, 'countdown': 5, 'lane': 4},
                {'size': 6, 'countdown': 6, 'lane': 5},
                {'size': 7, 'countdown': 7, 'lane': 6},
                {'size': 8, 'countdown': 8, 'lane': 7}]
  build_columns(squ_matrix, max_beat)
  dwg.save()

# (execfile('sonakinatography.py'))
# matrix_traverser(10)

# dwg.save()
