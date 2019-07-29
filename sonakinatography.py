import svgwrite

############## Setup

def write_svg(svg, path):
  with open(path, "w") as f:
    f.write(svg.tostring())
  return {'kind': 'file', 'content_type': 'image/svg+xml', 'coder': 'svg'}

############# Painter

def print_square(square):
  print(square['color'])

def print_line():
  print("|")

class Shape:

  # TODO: Adjust colors correctly

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

  def paint_square_to_group(self, canvas, group):
    group.add(canvas.rect((self.x, self.y), (self.square_size, self.square_size), fill=self.color_grid[self.color]))

  def paint_line(self, canvas):
    self.x = self.x + (self.square_size / 2) - 2
    canvas.add(canvas.rect((self.x, self.y), (3, self.square_size), fill=self.color_grid[self.color]))

  def paint_line_to_group(self, canvas, group):
    self.x = self.x + (self.square_size / 2) - 2
    group.add(canvas.rect((self.x, self.y), (3, self.square_size), fill=self.color_grid[self.color]))

##### Simple Example

def simple_shapes(shape1, shape2):
  dwg_shapes = svgwrite.Drawing('dwg_shapes.svg', (160,20))

  Shape(shape1).paint_square(dwg_shapes)
  Shape(shape2).paint_line(dwg_shapes)

  return dwg_shapes

##### Sonakinatography Builder

color_grid = [[2, 3, 4, 5, 6, 7, 8, 1],
              [3, 4, 5, 6, 7, 8, 1, 2],
              [4, 5, 6, 7, 8, 1, 2, 3],
              [5, 6, 7, 8, 1, 2, 3, 4],
              [6, 7, 8, 1, 2, 3, 4, 5],
              [7, 8, 1, 2, 3, 4, 5, 6],
              [8, 1, 2, 3, 4, 5, 6, 7],
              [1, 2, 3, 4, 5, 6, 7, 8]]
color_grid_max_y = len(color_grid)-1

def change_advancer(color_grid_y, func):
  if color_grid_y == color_grid_max_y:
    func = lambda y: y-1
  elif color_grid_y == 0:
    func = lambda y: y+1
  return func

def reset_instrument(instrument):
  instrument['advancer'] = change_advancer(instrument['color_grid_val'], instrument['advancer'])
  instrument['color_grid_val'] = instrument['advancer'](instrument['color_grid_val'])
  instrument['countdown'] = color_grid[instrument['color_grid_val']][instrument['instrument']-1]

def build_row(canvas, shape_group, grid_objects, beat, max_beat):
  for instrument in grid_objects:
    instrument['countdown'] -= 1
    instrument['color'] = color_grid[instrument['color_grid_val']][instrument['instrument']-1]
    shape = Shape(instrument, beat, max_beat)
    if instrument['countdown'] == 0:
      shape.paint_square_to_group(canvas, shape_group)
      # shape.paint_square(canvas)
      reset_instrument(instrument)
    else:
      shape.paint_line_to_group(canvas, shape_group)
#      shape.paint_line(canvas)

def build_columns(canvas, shape_group, grid_objects, max_beat):
  beat = 0
  while beat < max_beat:
    beat += 1
    build_row(canvas, shape_group, grid_objects, beat, max_beat)

def build_matrix(max_beat):
  canvas = svgwrite.Drawing('sonakinatography.svg', profile='tiny')
  group = canvas.add(canvas.g())

  # TODO: Update reset_instrument and create a software instantiation so that instrument x can start at any number.
  grid_objects = [{'color': 1, 'countdown': 1, 'instrument': 1, 'advancer': lambda y: y-1, 'color_grid_val': 7},
                  {'color': 2, 'countdown': 2, 'instrument': 2, 'advancer': lambda y: y-1, 'color_grid_val': 7},
                  {'color': 3, 'countdown': 3, 'instrument': 3, 'advancer': lambda y: y-1, 'color_grid_val': 7},
                  {'color': 4, 'countdown': 4, 'instrument': 4, 'advancer': lambda y: y-1, 'color_grid_val': 7},
                  {'color': 5, 'countdown': 5, 'instrument': 5, 'advancer': lambda y: y-1, 'color_grid_val': 7},
                  {'color': 6, 'countdown': 6, 'instrument': 6, 'advancer': lambda y: y-1, 'color_grid_val': 7},
                  {'color': 7, 'countdown': 7, 'instrument': 7, 'advancer': lambda y: y-1, 'color_grid_val': 7},
                  {'color': 8, 'countdown': 8, 'instrument': 8, 'advancer': lambda y: y-1, 'color_grid_val': 7}]
  build_columns(canvas, group, grid_objects, max_beat)

  # TODO: This currently animates the sonakinatography in an ugly way. Refactor and polish animation.

  group.add(canvas.animateTransform("translate","transform",id="polygon",from_="0,0", to="0,450",dur="4s",begin="0s",repeatCount="indefinite"))
  return canvas

def run_simple():
  draw = simple_shapes({'color': 2, 'instrument': 1}, {'color': 2, 'instrument': 3})
  draw.save()

def run_full(no_of_beats):
  draw = build_matrix(no_of_beats)
  draw.save()

# (execfile('sonakinatography.py'))

def run_animate():

    # Simple animation test

    canvas = svgwrite.Drawing('results/animation-test.svg',profile='tiny',size=(600,400))

    def add_instrument_to_group(canvas, shape_group, instrument):
      shape = Shape(instrument, 1, 1)
      shape.paint_line_to_group(canvas, shape_group)

    group = canvas.add(canvas.g())

    add_instrument_to_group(canvas, group, {'color': 1, 'countdown': 1, 'instrument': 1, 'advancer': lambda y: y-1, 'color_grid_val': 7})
    add_instrument_to_group(canvas, group, {'color': 1, 'countdown': 1, 'instrument': 7, 'advancer': lambda y: y-1, 'color_grid_val': 7})

    group.add(canvas.animateTransform("translate","transform",id="polygon",from_="0,0", to="0,450",dur="4s",begin="0s",repeatCount="indefinite"))

    canvas.save()
