import time
from collections import deque
import random

def rotate_piece(piece):
    return [list(row) for row in zip(*piece[::-1])]

def precompute_rotations(pieces):
    all_rotations = []
    for piece in pieces:
        rotations = []
        current = piece
        for _ in range(4):
            if current not in rotations:
                rotations.append(current)
            current = rotate_piece(current)
        all_rotations.append(rotations)
    return all_rotations

def piece_area(piece):
    return sum(sum(row) for row in piece)

def is_valid(grid, r, c, blocked_areas):
    """
    Return True if row r and column c are in-bounds for grid[r],
    and that cell is not blocked.
    """
    if r < 0 or r >= len(grid):
        return False
    if c < 0 or c >= len(grid[r]):
        return False
    # Check for blocked
    if (r, c) in blocked_areas:
        return False
    return True

def find_contiguous_regions(grid, blocked_areas):
    rows = len(grid)
    visited = []
    for r in range(rows):
        visited.append([False] * len(grid[r]))  # visited[r] has same width as grid[r]
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    regions = []

    for r in range(rows):
        for c in range(len(grid[r])):  # only iterate up to len(grid[r])
            if not visited[r][c] and grid[r][c] == 0 and (r,c) not in blocked_areas:
                # BFS/DFS to find all connected empty cells
                queue = deque([(r, c)])
                visited[r][c] = True
                size = 0

                while queue:
                    x, y = queue.popleft()
                    size += 1
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if is_valid(grid, nx, ny, blocked_areas):
                            if not visited[nx][ny] and grid[nx][ny] == 0:
                                visited[nx][ny] = True
                                queue.append((nx, ny))

                regions.append(size)
    return regions

def has_enough_space(grid, blocked_areas, piece_areas, index):
    # The pieces we have not placed yet:
    remaining_areas = piece_areas[index:]
    if not remaining_areas:
        return True  # no pieces left
    smallest_area = min(remaining_areas)
    
    regions = find_contiguous_regions(grid, blocked_areas)
    # If we find a region that is > 0 and < smallest_area => prune
    for size in regions:
        if 0 < size < smallest_area:
            return False
    return True

def solve_puzzle(grid, pieces, blocked_areas):
    blocked_areas_set = set(blocked_areas)

    # Pre-calculate the area of each original piece
    piece_areas = []
    for rotations in pieces:
        # All rotations have same area
        piece_areas.append(piece_area(rotations[0]))

    def can_place(grid, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] == 1:
                    nx, ny = x + i, y + j
                    # Check bounds for each row individually
                    if not is_valid(grid, nx, ny, blocked_areas_set):
                        return False
                    # If grid cell is non-zero => can't place
                    if grid[nx][ny] != 0:
                        return False
        return True

    def place_piece(grid, piece, x, y, value):
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] == 1:
                    grid[x + i][y + j] = value

    def backtrack(grid, pieces, index):
        if index == len(pieces):
            return True  # All pieces placed

        # Early prune
        if not has_enough_space(grid, blocked_areas_set, piece_areas, index):
            return False

        piece_rotations = pieces[index]
        label = chr(65 + index)

        for rotation in piece_rotations:
            # We must check row-by-row for valid placements
            for r in range(len(grid)):
                for c in range(len(grid[r])):
                    if can_place(grid, rotation, r, c):
                        place_piece(grid, rotation, r, c, label)
                        if backtrack(grid, pieces, index + 1):
                            return True
                        place_piece(grid, rotation, r, c, 0)
        return False

    if backtrack(grid, pieces, 0):
        return True, grid
    else:
        return False, None

if __name__ == "__main__":
    import time

    # Example of a "jagged" grid with mismatched row lengths
    origGrid = [
        [0, 0, 0, 0, 0, 0],   # 6 columns
        [0, 0, 0, 0, 0, 0],   # 6 columns
        [0, 0, 0, 0, 0, 0, 0],# 7 columns
        [0, 0, 0, 0, 0, 0, 0],# 7 columns
        [0, 0, 0, 0, 0, 0, 0],# 7 columns
        [0, 0, 0, 0, 0, 0, 0],# 7 columns
        [0, 0, 0],            # 3 columns
    ]

    pieces = [
        [
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 1]
        ],
        [
            [1, 1],
            [0, 1],
            [1, 1]
        ],
        [
            [0, 1],
            [0, 1],
            [0, 1],
            [1, 1]
        ],
        [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ],
        [
            [1, 0],
            [1, 1],
            [1, 1]
        ],
        [
            [1, 1],
            [1, 1],
            [1, 1]
        ],
        [
            [1, 0],
            [1, 1],
            [0, 1],
            [0, 1]
        ],
        [
            [0, 1],
            [1, 1],
            [0, 1],
            [0, 1]
        ],
    ]

    blocked_areas = [(0, 0), (4, 1)]  # Some blocked cells
    
    foundSolutions = 0
    maxSolutions = 1

    while foundSolutions < maxSolutions:
        grid = [row[:] for row in origGrid]
        start_time = time.time()
        all_rotations = precompute_rotations(pieces)
        success, solved_grid = solve_puzzle(grid, all_rotations, blocked_areas)
        if success and solved_grid:
            print("Puzzle solved:")
            for row in solved_grid:
                print("".join(str(cell) if cell != 0 else "." for cell in row))
        else:
            print("Puzzle cannot be solved.")
        print("--- %s seconds ---" % (time.time() - start_time))

        foundSolutions += 1
        # randomize the order of pieces
        random.shuffle(pieces)

