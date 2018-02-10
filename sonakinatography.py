import svgwrite

############## Setup

def write_svg(svg, path):
  with open(path, "w") as f:
    f.write(svg.tostring())
  return {'kind': 'file', 'content_type': 'image/svg+xml', 'coder': 'svg'}

############# Painter

def print_square(square):
  print square['size'],

def print_line():
  print "|",

class Shape:

  yellow_green=svgwrite.rgb(0, 204, 0)   # Yellow Green
  green=svgwrite.rgb(0, 102, 0)          # Green
  blue=svgwrite.rgb(0, 0, 255)           # Blue
  blue_violet=svgwrite.rgb(127, 0, 255)  # Blue Violet
  red_violet=svgwrite.rgb(153, 0, 153)   # Red Violet
  red=svgwrite.rgb(204, 0, 0)            # Red
  orange=svgwrite.rgb(255, 128, 0)       # Orange
  yellow=svgwrite.rgb(255, 255, 0)       # Yellow

  color_grid = [yellow_green, green, blue, blue_violet, red_violet, red, orange, yellow]

  square_size = 20

  def scale_square(self, x, y):
    return ((x*self.square_size), (y*self.square_size))

  def __init__(self, lane, beat, max_beat):
    self.color = (lane['size'] - 1)
    self.x, self.y = self.scale_square(lane['lane'], beat)
    self.y = abs(self.y - (max_beat * self.square_size))

  def paint_square(self, canvas):
    canvas.add(canvas.rect((self.x, self.y), (self.square_size, self.square_size), fill=self.color_grid[self.color]))

  def paint_line(self, canvas):
    self.x = self.x + (self.square_size / 2) - 2
    canvas.add(canvas.rect((self.x, self.y), (3, self.square_size), fill=self.color_grid[self.color]))

# Builder

def reset_lane(lane):
  if lane['size'] == 1:
    lane['size'] = 8
  else:
    lane['size'] -= 1
  lane['countdown'] = lane['size']
  return lane

def build_row(canvas, grid_objects, beat, max_beat):
  for lane in grid_objects:
    lane['countdown'] -= 1
    shape = Shape(lane, beat, max_beat)
    if lane['countdown'] == 0:
      shape.paint_square(canvas)
      lane = reset_lane(lane)
    else:
      shape.paint_line(canvas)

def build_columns(canvas, grid_objects, max_beat):
  beat = 0
  while beat < max_beat:
    beat += 1
    build_row(canvas, grid_objects, beat, max_beat)

def simple_shapes():
  dwg_shapes = svgwrite.Drawing('dwg_shapes.svg', profile='tiny')
  grid_object1 = {'size': 1, 'lane': 0}
  shape1 = Shape(grid_object1, 1, 1)
  shape1.paint_square(dwg_shapes)

  grid_object2 = {'size': 1, 'lane': 1}
  shape2 = Shape(grid_object2, 1, 1)
  shape2.paint_line(dwg_shapes)

  dwg_shapes.save()

def matrix_traverser(max_beat):
  dwg = svgwrite.Drawing('test.svg', profile='tiny')

  grid_objects = [{'size': 1, 'countdown': 1, 'lane': 0},
                  {'size': 2, 'countdown': 2, 'lane': 1},
                  {'size': 3, 'countdown': 3, 'lane': 2},
                  {'size': 4, 'countdown': 4, 'lane': 3},
                  {'size': 5, 'countdown': 5, 'lane': 4},
                  {'size': 6, 'countdown': 6, 'lane': 5},
                  {'size': 7, 'countdown': 7, 'lane': 6},
                  {'size': 8, 'countdown': 8, 'lane': 7}]
  build_columns(dwg, grid_objects, max_beat)
  dwg.save()

# (execfile('sonakinatography.py'))
# matrix_traverser(30)
