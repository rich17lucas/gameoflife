#!/usr/bin/env python3
import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON,OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.3, 0.7]).reshape(N, N)

def addGlider(i, j, grid):
    """Adds a glider with top-left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                      [255, 0, 255],
                      [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider

def addShark(i, j, grid):
    """Adds a shark with top-left cell at (i,j)"""
    shark = np.array([[255,255,0,],
                     [0,255,0],
                     [255,0,0]])
    grid[i:i+3, j:j+3] = shark
    
def update(frameNum, img, grid, N):
    # Copy grid since we require 8 neighbours for calculation
    # and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8 neighbor sum using toroidal boundary conditions
            # x and y wrap around so that the simulation
            # takes place on a toroidal surface
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            # Apply Conway's rules
            if grid[i,j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i,j] = OFF
            else:
                if total == 3:
                    newGrid[i,j] = ON

            # Apply a random mutation
            rdm = np.random.uniform(0.0,1.0,1)
                        
            if rdm  < 0.00002:
                if newGrid[i,j] == OFF:
                    newGrid[i,j] = ON
                else:
                    newGrid[i,j] = OFF
                    print("{} Random mutation at {},{}".format(rdm,i,j))
                    
            if rdm > 0.999995:
                try:
                    addGlider(i,j, newGrid)
                except Exception:
                    pass
                else:
                    print("{} Added glider at: {},{}".format(rdm,i,j))
    
            if 0.5 <= rdm <= 0.50001:
                try:
                    addShark(i,j, newGrid)
                except Exception:
                    pass
                else:
                    print("{} Added shark at: {},{}".format(rdm,i,j))
                    
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main function()
def main():
    # Command line arguments are held in sys.arg[1], sys.arg[2], ...
    # sys.argv[0] is the script name and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    # Add arguments
    parser.add_argument('--grid-size',  dest="N",           required=False)
    parser.add_argument('--mov-file',   dest="movfile",     required=False)
    parser.add_argument('--interval',   dest="interval",    required=False)
    parser.add_argument('--glider',     action="store_true",  required=False)
    parser.add_argument('--gosper',     action="store_true",  required=False)
    args = parser.parse_args()
    
    # Set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)
    
    # Set animation update interval (in ms)
    updateInterval = 50
    if args.interval and int(args.interval):
        updateInterval = int(args.interval)

    # Declare grid
    grid = np.array([])
    # Check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(N*N).reshape(N,N)
        addGlider(1, 1, grid)
    else:
        # Populate grid with random on/off - more off than on
        grid = randomGrid(N)

    # Set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap='copper')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = 10,
                                  interval = updateInterval,
                                  save_count = 50)
    # number of frames?
    # set the output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
    
    plt.show()
    
# call main
if __name__ == '__main__':
    main()
