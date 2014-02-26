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

def grid_height(grid):
    width = len(grid)
    height = len(grid[0])

    configuration_height = 0

    for y in range(height):
        for x in range(width):
            if grid[x][y] == 'x':
                configuration_height = height - y
                return configuration_height / float(height)

    return 0

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

    return sides_touching / float(total_sides_touching)

def blockages(grid):
    width = len(grid)
    height = len(grid[0])

    blockages = 0

    for x in range(width):
        for y in range(1, height):
            if grid[x][y] != 'x':
                k = y - 1
                while k >= 0:
                    if grid[x][k] == 'x':
                        blockages += 1
                        break
                    k -= 1

    return blockages / float(height / 2 * width)


def rows_cleared(grid):
    width = len(grid)
    height = len(grid[0])
    num_rows_filled = 0

    for y in range(height):
        row_filled = True
        for x in range(width):
            if grid[x][y] != 'x':
                row_filled = False
                break
        if row_filled:
            num_rows_filled += 1

    return num_rows_filled / float(height)

def calculate_fitness(grid, weights):
    fitness_functions = [sides_touching, grid_height, rows_cleared, blockages]
    fitness_value = 0

    # print ' ============ '
    for i in range(len(weights)):
        fitness_function_value = fitness_functions[i](grid)
        # print '{} --- {}'.format(fitness_functions[i].__name__, fitness_function_value * weights[i])
        fitness_value += weights[i] * fitness_function_value

    return fitness_value

