import numpy as np
from environment import Environment
import environment
from environment import Point
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
import math

# f = g + h

# What information do i need in each element of the matrix?
# g definitely
# h maybe?
# [0-8] value in which direction the parent is (0, is itself, 1, north, then counterclockwise)

# Point is an array with 2 elements. The 0th is x, the 1st is y

# Access to map array and environment is with matrix notation and not cartesian access. map[row, column] not map[x, y]

#def parseDirection(point, parent


class MapInfo:
    def __init__(self):
        self.g = -1
        self.h = -1
        self.par = []
        self.queuePoint = False
    
    def setInfo(self, g = None, h = None, par = None):
        if g != None:
            self.g = g
        if h != None:
            self.h = h
        if par != None:
            self.par = par
    
    def getTotalHeuristic(self):
        return self.g + self.h
    
    def containsValidInfo(self):
        if self.h != -1 or self.g != -1:
            return True

    def printInfo(self):
        print(f"[g, h, par] is: [{self.g}, {self.h}, {self.par}]")


class AStarMethod():
    def __init__(self, environment):
        self.env = environment.environment
        self.map = np.empty((self.env.shape[0], self.env.shape[1]), dtype=object)
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                self.map[i, j] = MapInfo()
        self.start = environment.startpos
        self.end = environment.endpos
        self.map[self.start.y, self.start.x].setInfo(g = 0, h = self.endHeuristic(self.start, self.end))
        self.frontier_queue = [[self.start, self.map[self.start.y, self.start.x].getTotalHeuristic()]]
    
    def endHeuristic(self, point, end): # h
        dx = abs(end.x - point.x)
        dy = abs(end.y - point.y)
        return math.sqrt(dx ** 2 + dy ** 2)
    
    def getStartHeuristic(self, point, parent):
        g_add = math.sqrt((point.x - parent.x) ** 2 + (point.y - parent.y) ** 2)
        return self.map[parent.y, parent.x].g + g_add


    def updateMapPointInfo(self, point, parent):
        dir = parent
        self.map[point.y, point.x].g = self.getStartHeuristic(point, parent)
        self.map[point.y, point.x].h = self.endHeuristic(point, self.end)
        self.map[point.y, point.x].par = dir

    def updateFrontierQueuePoint(self, point):
        if self.map[point.y, point.x].g == -1:
            raise RuntimeError("Trying to update frontier for a point which has no information!")
        pointTotalHeuristic = self.map[point.y, point.x].getTotalHeuristic()
        if len(self.frontier_queue) == 0:
            self.frontier_queue.insert(0, [point, pointTotalHeuristic])
        if self.map[point.y, point.x].queuePoint is True:
            for i in range(len(self.frontier_queue)):
                elem = self.frontier_queue[i]
                if elem[0].x == point.x and elem[0].y == point.y:
                    if elem[1] <= pointTotalHeuristic:
                        return
                    else:
                        self.frontier_queue.pop(i)
                        break
        for i in range(len(self.frontier_queue)):
            if self.frontier_queue[i][1] >= self.map[point.y, point.x].getTotalHeuristic():
                self.frontier_queue.insert(i, [point, self.map[point.y, point.x].getTotalHeuristic()])
                self.map[point.y, point.x].queuePoint = True
                break







    #def get_shortest_path(self, start, end):
        # Add frontier elements

        # Execute Frontier

        # Update Information
    
    def addNewFrontierElements(self, point):
        for rel_row in range(-1, 2, 1): #list from -1 to 1 for relative row 
            for rel_col in range(-1, 2, 1): #list from -1 to 1 for relative column
                eval_point = Point(point.x + rel_col, point.y + rel_row)
                eval_point_g = self.getStartHeuristic(eval_point, point)
                if self.env[eval_point.y , eval_point.x] == 1 or (self.map[eval_point.y, eval_point.x].g <= eval_point_g and self.map[eval_point.y, eval_point.x].containsValidInfo()):
                    continue
                else:
                    self.updateMapPointInfo(eval_point, point)
                    self.updateFrontierQueuePoint(eval_point)

    def executeFrontierPoint(self):
        execPoint = self.frontier_queue.pop(0)[0]
        self.exec_point = execPoint
        self.map[self.exec_point.y, self.exec_point.x].queuePoint = False
        # print(f"Frontier is: \n{self.frontier_queue}")
        # print(f"execPoint is: {execPoint}")
        self.addNewFrontierElements(execPoint)

    def displayAlgorithm(self):
        fig, ax = plt.subplots(figsize= (10,10))
        cmap = colors.ListedColormap(['white', 'black'])

        ax.imshow(self.env, cmap=cmap)
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)

        ax.set_xticks(np.arange(0.5, self.env.shape[1], 1))
        ax.set_yticks(np.arange(0.5, self.env.shape[0], 1))
        plt.tick_params(axis='both', which='both', bottom=False,   
            left=False, labelbottom=False, labelleft=False)
        
        ax.scatter(self.start.x, self.start.y, marker='x', color = 'red', s=80)
        ax.scatter(self.end.x, self.end.y, marker='*', color = 'red', s = 80)
        ax.scatter(self.exec_point.x, self.exec_point.y, color='grey')
        for elem in self.frontier_queue:
            ax.scatter(elem[0].x, elem[0].y, marker='o', color = 'blue')
        #ani = animation.FuncAnimation(fig=fig, func=self.executeFrontierPoint)
        # Print environemnt, then all frontier points, and where i currently am
        plt.show()
        





                    



    
    #def shortest_path_iteration(self, point):



#Setup Environment
env = Environment(50, 50)
env.addblockrow(20, 35, 20)
env.addblockrow(10, 10, 15)
env.addblockcolumn(10, 20, 10)
env.addblockcolumn(22, 5, 20)
env.setstartpos(10, 5)
env.endpos(30, 40)
#env.plotenvironment()
astar = AStarMethod(env)
astar.executeFrontierPoint()
astar.displayAlgorithm()
#for i in range(0, 10):
#    astar.executeFrontierPoint()
#    astar.displayAlgorithm()
#    print("\n\n\n")


