import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap

MODE = "ROOK"
MAXSTEPS = 10000

DPI = 72
width, height = 700, 525
fig, ax = plt.subplots(figsize=(width/DPI, height/DPI), dpi=DPI)
ax.axis('square')

# spiral starts to the right (i.e., (1,0) = 2)
# spiral goes counterclockwise
# diagonals:
# 4n^2 - 2n + 1 is (n, n)
# 4n^2 + 4n + 1 is (n, -n)
# 4n^2 + 2n + 1 is (-n, -n)
# 4n^2 + 1 is (-n, n)

def coord_to_label(x, y):
    # which diagonal quadrant are we in?
    if abs(x) > abs(y):
        # left or right quadrant
        if x >= 0:
            # right
            value_on_diagonal = 4*x**2 - 2*x + 1
            down_steps = (x-y)
            return value_on_diagonal - down_steps
        else:
            # left
            value_on_diagonal = 4*x**2 + 2*abs(x) + 1
            up_steps = (y-x)
            return value_on_diagonal - up_steps
    else:
        # top or bottom quadrant
        if y >= 0:
            # top
            value_on_diagonal = 4*y**2 + 1
            right_steps = (x+y)
            return value_on_diagonal - right_steps
        else:
            # bottom
            value_on_diagonal = 4*y**2 + 4*abs(y) + 1
            left_steps = (-x-y)
            return value_on_diagonal - left_steps

def get_moves(iy, ix):
    if MODE == "ROOK":
        move_length = len(str(max(abs(ix),abs(iy)))) + 1
        return (move_length,0), (0,move_length), (-move_length,0), (0,-move_length)
    elif MODE == "BISHOP":
        move_length = len(str(max(abs(ix),abs(iy)))) + 1
        return (move_length,move_length), (-move_length,move_length), (-move_length,-move_length), (move_length,-move_length)
    elif MODE == "QUEEN":
        move_length = len(str(max(abs(ix),abs(iy)))) + 1
        return (move_length,0), (0,move_length), (-move_length,0), (0,-move_length), (move_length,move_length), (-move_length,move_length), (-move_length,-move_length), (move_length,-move_length)
    elif MODE == "KNIGHT":
        return (-1,-2), (-1,2), (1,-2), (1,2), (-2,-1), (-2,1), (2,-1), (2,1)
    else:
        raise ValueError("Please specify a valid piece configuration (line 6)") 


def get_next(iy, ix):
    next_sq = []
    
    for dy, dx in get_moves(iy, ix):
        jy, jx = iy + dy, ix + dx
        if (jy, jx) not in visited:
            next_sq.append((jy, jx))
    if not next_sq:
        # No valid moves – we're done: return None
        return
    return min(next_sq, key=lambda e: coord_to_label(e[1],e[0]))

# Keep track of the visited squares' indexes in the list visited.
visited = []
iy, ix = 0, 0
i = 0
# Run the game until there are no valid moves and print the visited squares.
while True:
    i += 1
    visited.append((iy, ix))
    try:
        iy, ix = get_next(iy, ix)
        # print("(" + str(iy) + ", " + str(ix) + ") " + str(coord_to_label(ix, iy)))
    except TypeError:
        break
    if i % (MAXSTEPS/100) == 0:
        print(str(i/MAXSTEPS*100) + "%")
    if i > MAXSTEPS:
        break
print(', '.join(str(coord_to_label(ix, iy)) for iy, ix in visited))
print('Done in {} steps'.format(i))

# Plot the path of the knight on a chessboard in a pleasing colour scheme.
points = np.array(visited).reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
norm = plt.Normalize(1, len(visited))
lc = LineCollection(segments, cmap='plasma_r', norm=norm)
lc.set_array(np.array(range(len(visited))))
line = ax.add_collection(lc)

ax.scatter([visited[0][0], visited[-1][0]], [visited[0][1], visited[-1][1]],
           c=('g','r'), marker='x', zorder=10)

ptp = np.concatenate( (np.min(points[:,:], axis=0),
                       np.max(points[:,:], axis=0)) ).T

ax.set_xlim(ptp[0][0]-0.5, ptp[0][1]+0.5)
ax.set_ylim(ptp[1][0]-0.5, ptp[1][1]+0.5)

xmin, xmax = ptp[0]
ymin, ymax = ptp[1]
board = np.zeros((ymax-ymin+1, xmax-xmin+1), dtype=int)
board[1::2, ::2] = 1
board[::2, 1::2] = 1

cmap = ListedColormap(['#aaaaaa', 'white'])

ax.imshow(board, extent=[xmin-0.5,xmax+0.5,ymin-0.5,ymax+0.5], cmap=cmap)

plt.savefig('traavelling-chess-piece.png', dpi=DPI)
plt.show()
