def get_neighbors(x, y, width, height):
    neighbors = []

    for j in range(-1, 2, 1):
        for k in range(-1, 2, 1):
            x_val = (x + j)
            y_val = (y + k)

            if x_val < 0 or x_val >= width:
                continue
            elif y_val < 0 or y_val >= height:
                continue
            elif x_val == 0 and y_val == 0:
                continue
            else:
                neighbors.append((x_val, y_val))

    return neighbors

def sides_touching(grid):
    width = len(grid)
    height = len(grid[0])

    sides_touching = 0
    total_sides_touching = 0

    for x in range(width):
        for y in range(height):
            neighbors = get_neighbors(x, y, width, height)
            for neighbor_x, neighbour_y in neighbors:
                if grid[neighbor_x][neighbour_y] == 'x':
                    sides_touching += 1
                total_sides_touching += 1

    return sides_touching / float(total_sides_touching)


def calculate_fitness(grid, weights):
    fitness_functions = [sides_touching]
    fitness_value = 0

    for i in range(len(weights)):
        fitness_value += weights[i] * fitness_functions[i](grid)

    return fitness_value

