from fitness import calculate_fitness


width = 10
height = 22
grid = []

for x in range(width):
    empty_column = []
    for y in range(height):
        empty_column.append('-')
    grid.append(empty_column)

with open('grid.dat') as f:
    y = 0
    for line in f:
        if len(line) < width:
            break

        x = 0
        for cell in line:
            if cell == 'x':
                grid[x][y] = 'x'
            x += 1
        y += 1

print calculate_fitness(grid, [7, -7, 5, -6])
