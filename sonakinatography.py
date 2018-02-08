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

square_size = 20
square_state = [[5, 5, 4, 4, 5, 6, 6, 6],
                [red, green, green, yellow_green, blue_violet, red_violet, orange, yellow]]
grid_size = len(square_state[0])

number_grid = [[2, 3, 4, 5, 6, 7, 8, 1],
               [3, 4, 5, 6, 7, 8, 1, 2],
               [4, 5, 6, 7, 8, 1, 2, 3],
               [5, 6, 7, 8, 1, 2, 3, 4],
               [6, 7, 8, 1, 2, 3, 4, 5],
               [7, 8, 1, 2, 3, 4, 5, 6],
               [8, 1, 2, 3, 4, 5, 6, 7],
               [1, 2, 3, 4, 5, 6, 7, 8]]
color_grid = [green, blue, blue_violet, red_violet, red, orange, yellow, yellow_green]
number_grid_max_y = len(number_grid)-1
grid_state = number_grid[number_grid_max_y]

# Builder

def change_advancer(number_grid_y, func):
  if number_grid_y == number_grid_max_y:
    func = lambda y: y-1
  elif number_grid_y == 0:
    func = lambda y: y+1
  return func

def grid_reader(number_grid_y):
  return abs(number_grid_y - number_grid_max_y)

def print_grid_state(grid_state):
  for x in grid_state:
    if x-1 == 0:
      print "v",
    else:
      print "|",
  print("")

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

############## Functions

def scale_square(x, y, offset):
  return ((x*square_size)+offset), ((y*square_size)+offset)

def grid(x,y,grid_size,offset):
  if y <= grid_size:
    x1,y1 = scale_square(grid_size,y,offset)
    dwg.add(dwg.line((offset, y1), (x1,y1), stroke=svgwrite.rgb(156, 156, 156)))
    grid(x,(y+1),grid_size,offset)
  elif x <= grid_size:
    x1,y1 = scale_square(x,grid_size,offset)
    dwg.add(dwg.line((x1, offset), (x1,y1), stroke=svgwrite.rgb(156, 156, 156)))
    grid((x+1),y,grid_size,offset)

def square_placer(horiz,offset):
  horiz = horiz - 1
  if horiz >= 0:
    x, y = scale_square(horiz,square_state[0][horiz],offset)
    dwg.add(dwg.rect((x, y), (square_size,square_size), fill=square_state[1][horiz]))
    square_placer(horiz,offset)

############## Create

grid (0,0,grid_size,0)
square_placer(grid_size,0)

dwg.save()
