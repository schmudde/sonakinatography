############## Simple Grid and Square Placer

square_size = 20
square_state = [[5, 5, 4, 4, 5, 6, 6, 6],
                [red, green, green, yellow_green, blue_violet, red_violet, orange, yellow]]
grid_size = len(square_state[0])

def scale_square(x, y, offset):
  return ((x*square_size)+offset), ((y*square_size)+offset)

def grid(x,y,grid_size,offset):

  # Example call: grid (0,0,grid_size,0)

  if y <= grid_size:
    x1,y1 = scale_square(grid_size,y,offset)
    dwg.add(dwg.line((offset, y1), (x1,y1), stroke=svgwrite.rgb(156, 156, 156)))
    grid(x,(y+1),grid_size,offset)
  elif x <= grid_size:
    x1,y1 = scale_square(x,grid_size,offset)
    dwg.add(dwg.line((x1, offset), (x1,y1), stroke=svgwrite.rgb(156, 156, 156)))
    grid((x+1),y,grid_size,offset)

def square_placer(horiz,offset):

  # Example call: square_placer(grid_size,0)

  horiz = horiz - 1
  if horiz >= 0:
    x, y = scale_square(horiz,square_state[0][horiz],offset)
    dwg.add(dwg.rect((x, y), (square_size,square_size), fill=square_state[1][horiz]))
    square_placer(horiz,offset)

############## Place Using Channa's Grid Layout

number_grid = [[2, 3, 4, 5, 6, 7, 8, 1],
               [3, 4, 5, 6, 7, 8, 1, 2],
               [4, 5, 6, 7, 8, 1, 2, 3],
               [5, 6, 7, 8, 1, 2, 3, 4],
               [6, 7, 8, 1, 2, 3, 4, 5],
               [7, 8, 1, 2, 3, 4, 5, 6],
               [8, 1, 2, 3, 4, 5, 6, 7],
               [1, 2, 3, 4, 5, 6, 7, 8]]
number_grid_max_y = len(number_grid)-1
grid_state = number_grid[number_grid_max_y]

def grid_reader(number_grid_y):
  return abs(number_grid_y - number_grid_max_y)

def print_grid_state(grid_state):
  for x in grid_state:
    if x-1 == 0:
      print("v")
    else:
      print("|")
  print("")
