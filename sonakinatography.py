import svgwrite

############## Setup

def write_svg(svg, path):
  with open(path, "w") as f:
    f.write(svg.tostring())
  return {'kind': 'file', 'content_type': 'image/svg+xml', 'coder': 'svg'}

dwg = svgwrite.Drawing('test.svg', profile='tiny')

green=svgwrite.rgb(0, 204, 0)          # Green
blue=svgwrite.rgb(0, 0, 255)           # Blue
blue_violet=svgwrite.rgb(127, 0, 255)  # Blue Violet
red_violet=svgwrite.rgb(153, 0, 153)   # Red Violet
red=svgwrite.rgb(204, 0, 0)            # Red
orange=svgwrite.rgb(255, 128, 0)       # Orange
yellow=svgwrite.rgb(255, 255, 0)       # Yellow
yellow_green=svgwrite.rgb(0, 102, 0)   # Yellow Green

color_grid = [green, blue, blue_violet, red_violet, red, orange, yellow, yellow_green]

# Builder

def paint_square(square):
  print square['size'],

def reset_square(square):
  if square['size'] == 1:
    square['size'] = 8
  else:
    square['size'] -= 1
  square['countdown'] = square['size']
  return square

def build_row(squ_matrix):
  for square in squ_matrix:
    square['countdown'] -= 1
    if square['countdown'] == 0:
      paint_square(square)
      square = reset_square(square)
    else:
      print "|",
  return squ_matrix

def build_columns(squ_matrix, max_beat):
  i = 0
  while i < max_beat:
    i += 1
    squ_matrix = build_row(squ_matrix)
    print(" ")

def matrix_traverser(max_beat):
  squ_matrix = [{'size': 1, 'countdown': 1},
                {'size': 2, 'countdown': 2},
                {'size': 3, 'countdown': 3},
                {'size': 4, 'countdown': 4},
                {'size': 5, 'countdown': 5},
                {'size': 6, 'countdown': 6},
                {'size': 7, 'countdown': 7},
                {'size': 8, 'countdown': 8}]
  build_columns(squ_matrix, max_beat)

# (execfile('sonakinatography.py'))
# matrix_traverser(10)

dwg.save()
