from astarmethod import AStarMethod
from astarmethod import AstarStatus
from environment import Environment
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
import numpy as np

def frameGen(astar):
    while astar.status == AstarStatus.RUNNING:
        print(f"Status is: {astar.status}")
        yield None

def createAnimation(astar):
    global ani
    fig, ax = plt.subplots(figsize= (10,10))
    cmap = colors.ListedColormap(['white', 'black'])
    plt.title("Occupancy Map")
    ax.imshow(astar.env, cmap=cmap)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
    
    ax.set_xticks(np.arange(0.5, astar.env.shape[1], 1))
    ax.set_yticks(np.arange(0.5, astar.env.shape[0], 1))
    plt.tick_params(axis='both', which='both', bottom=False,   
        left=False, labelbottom=False, labelleft=False)
    ax.scatter(astar.start.x, astar.start.y, marker='*', color = 'red', s=80, label="Start Point")
    ax.scatter(astar.end.x, astar.end.y, marker='*', color = 'red', s = 80, label="End Point")

    frontier_scatter = ax.scatter([], [], marker='o', color='blue')
    execpoint_scatter = ax.scatter([], [], color = 'grey')
    currentexecpoint = ax.scatter([], [], marker = '*', color = 'black', s = 80)
    ax.legend()
    astar.initExecution()
    ani = animation.FuncAnimation(fig=fig, func=executeFrontierPointAnimation, fargs=(astar, frontier_scatter, execpoint_scatter, currentexecpoint, ax), frames=frameGen(astar))

    ani.save('astarplanner.gif', writer='pillow')
    plt.show()
    
def endAnimation(astar, ax):
    x_plot, y_plot = astar.extractShortestPath()
    ax.plot(x_plot, y_plot)


def executeFrontierPointAnimation(_, astar, frontier_scatter, execpoint_scatter, currentexecpoint, ax):
    global ani
    if not astar.executeFrontierPoint():
        ani.event_source.stop() # End animation
        endAnimation(astar, ax)

    frontier_xy = [[entry[0].x, entry[0].y] for entry in astar.frontier_queue]
    frontier_scatter.set_offsets(frontier_xy)
    if astar.past_exec_points:
        execpoint_xy = [[entry.x, entry.y] for entry in astar.past_exec_points]
        execpoint_scatter.set_offsets(execpoint_xy)
    currentexecpoint.set_offsets([astar.exec_point.x, astar.exec_point.y])


#Setup Environment
env = Environment(45, 45)
env.addblockrow(20, 35, 20)
env.addblockrow(10, 10, 15)
env.addblockcolumn(10, 20, 10)
env.addblockcolumn(22, 5, 20)
env.setstartpos(10, 5)
env.endpos(30, 40)
astar = AStarMethod(env)

createAnimation(astar)
