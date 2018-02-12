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
    x -= 1 # Start the x-axis scaling at 0, not 1
    return ((x*self.square_size), (y*self.square_size))

  def __init__(self, instrument, beat = 1, max_beat = 1):
    self.color = (instrument['color'] - 1)
    self.x, self.y = self.scale_square(instrument['instrument'], beat)
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

def reset_instrument(instrument):
  if instrument['color'] == 1:
    instrument['color'] = 8
  else:
    instrument['color'] -= 1
  instrument['countdown'] = instrument['color']
  return instrument

def build_row(canvas, grid_objects, beat, max_beat):
  for instrument in grid_objects:
    instrument['countdown'] -= 1
    shape = Shape(instrument, beat, max_beat)
    if instrument['countdown'] == 0:
      shape.paint_square(canvas)
      instrument = reset_instrument(instrument)
    else:
      shape.paint_line(canvas)

def build_columns(canvas, grid_objects, max_beat):
  beat = 0
  while beat < max_beat:
    beat += 1
    build_row(canvas, grid_objects, beat, max_beat)

def build_matrix(max_beat):
  dwg = svgwrite.Drawing('test.svg', profile='tiny')

  grid_objects = [{'color': 1, 'countdown': 1, 'instrument': 1},
                  {'color': 2, 'countdown': 2, 'instrument': 2},
                  {'color': 3, 'countdown': 3, 'instrument': 3},
                  {'color': 4, 'countdown': 4, 'instrument': 4},
                  {'color': 5, 'countdown': 5, 'instrument': 5},
                  {'color': 6, 'countdown': 6, 'instrument': 6},
                  {'color': 7, 'countdown': 7, 'instrument': 7},
                  {'color': 8, 'countdown': 8, 'instrument': 8}]
  build_columns(dwg, grid_objects, max_beat)
  return dwg

def run_simple():
  draw = simple_shapes({'color': 2, 'instrument': 1}, {'color': 2, 'instrument': 3})
  draw.save()

def run_full(no_of_beats):
  draw = build_matrix(no_of_beats)
  draw.save()

# (execfile('sonakinatography.py'))
# run_full(35)
