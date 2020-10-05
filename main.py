from grids import Grid
 
grid = Grid(5,3) # Create an empty 5x3 grid.
 
print(grid.get_cell(5,3)) # -> ∅ None
print(grid.get_cell(3,1)) # -> ∅ None
 
grid.update_cell(5,3,'Foo')
grid.update_cell(3,2,'Bar')
 
print(grid.view())