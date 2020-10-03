from grids import Grid
import os

grid = Grid.load('grid1.dat')

print(repr(grid))
print(grid.log)

os.remove('grid1.dat')
grid.save()
