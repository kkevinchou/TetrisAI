def get_neighbors(x, y, width, height):
    neighbors = []

    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for offset in offsets:
        out_of_grid = False

        x_val = (x + offset[0])
        y_val = (y + offset[1])

        if x_val < 0 or x_val >= width:
            out_of_grid = True
        elif y_val < 0 or y_val >= height:
            out_of_grid = True
        elif x_val == 0 and y_val == 0:
            continue

        neighbors.append((x_val, y_val, out_of_grid))

    return neighbors

def sides_touching(grid):
    width = len(grid)
    height = len(grid[0])

    sides_touching = 0
    total_sides_touching = 0

    for x in range(width):
        for y in range(height):
            if grid[x][y] != 'x':
                continue

            neighbors = get_neighbors(x, y, width, height)

            for neighbor_x, neighbour_y, out_of_grid in neighbors:
                if out_of_grid or grid[neighbor_x][neighbour_y] == 'x':
                    sides_touching += 1
                total_sides_touching += 1

    return sides_touching


def calculate_fitness(grid, weights):
    fitness_functions = [sides_touching]
    fitness_value = 0

    for i in range(len(weights)):
        fitness_value += weights[i] * fitness_functions[i](grid)

    return fitness_value

