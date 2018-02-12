import svgwrite

############## Setup

def write_svg(svg, path):
  with open(path, "w") as f:
    f.write(svg.tostring())
  return {'kind': 'file', 'content_type': 'image/svg+xml', 'coder': 'svg'}

############# Painter

def print_square(square):
  print square['color'],

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

  def __init__(self, lane, beat = 1, max_beat = 1):
    self.color = (lane['color'] - 1)
    self.x, self.y = self.scale_square(lane['lane'], beat)
    self.y = abs(self.y - (max_beat * self.square_size))

  def paint_square(self, canvas):
    canvas.add(canvas.rect((self.x, self.y), (self.square_size, self.square_size), fill=self.color_grid[self.color]))

  def paint_line(self, canvas):
    self.x = self.x + (self.square_size / 2) - 2
    canvas.add(canvas.rect((self.x, self.y), (3, self.square_size), fill=self.color_grid[self.color]))

##### Simple Example

def simple_shapes(shape1, shape2):
  dwg_shapes = svgwrite.Drawing('dwg_shapes.svg', (160,20))

  Shape(shape1).paint_square(dwg_shapes)
  Shape(shape2).paint_line(dwg_shapes)

  return dwg_shapes

##### Sonakinatography Builder

def reset_lane(lane):
  if lane['color'] == 1:
    lane['color'] = 8
  else:
    lane['color'] -= 1
  lane['countdown'] = lane['color']
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

def build_matrix(max_beat):
  dwg = svgwrite.Drawing('test.svg', profile='tiny')

  grid_objects = [{'color': 1, 'countdown': 1, 'lane': 0},
                  {'color': 2, 'countdown': 2, 'lane': 1},
                  {'color': 3, 'countdown': 3, 'lane': 2},
                  {'color': 4, 'countdown': 4, 'lane': 3},
                  {'color': 5, 'countdown': 5, 'lane': 4},
                  {'color': 6, 'countdown': 6, 'lane': 5},
                  {'color': 7, 'countdown': 7, 'lane': 6},
                  {'color': 8, 'countdown': 8, 'lane': 7}]
  build_columns(dwg, grid_objects, max_beat)
  return dwg

def run_simple():
  draw = simple_shapes({'color': 3, 'lane': 0}, {'color': 4, 'lane': 2})
  draw.save()

def run_full(no_of_beats):
  draw = build_matrix(no_of_beats)
  draw.save()

# (execfile('sonakinatography.py'))
# run_full(35)
