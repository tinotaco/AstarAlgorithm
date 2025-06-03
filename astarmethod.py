import numpy as np
from environment import Environment
import environment
from environment import Point
import math

global ani

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
        self.exec_point = []
        self.past_exec_points = []
        self.frontier_queue = []
    
    def initExecution(self):
        self.past_exec_points = []
        self.frontier_queue = []
        self.exec_point = self.start
        self.map[self.start.y, self.start.x].setInfo(g = 0, h = self.endHeuristic(self.start, self.end))
        self.addNewFrontierElements(self.start)
        print(f"New FrontierElements after init are: {self.frontier_queue}")

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
            self.map[point.y, point.x].queuePoint = True
            return
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
                added_value = True
                self.frontier_queue.insert(i, [point, self.map[point.y, point.x].getTotalHeuristic()])
                self.map[point.y, point.x].queuePoint = True
                return
        # Newest element contains largest value in frontier queue list therefore placed at back
        self.frontier_queue.append([point, self.map[point.y, point.x].getTotalHeuristic()])
        self.map[point.y, point.x].queuePoint = True
        
    
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
        self.past_exec_points.append(Point(self.exec_point.x, self.exec_point.y))
        execPoint = self.frontier_queue.pop(0)[0]
        self.exec_point = execPoint
        if self.exec_point.x == self.end.x and self.exec_point.y == self.end.y:
            return False # The end point has been reached, stop algorithm
        self.map[self.exec_point.y, self.exec_point.x].queuePoint = False
        self.addNewFrontierElements(execPoint)
        return True
    
    def extractShortestPath(self):
        if not self.map[self.end.y, self.end.x].containsValidInfo():
            raise RuntimeError("Trying to get shortest path but end point has not been evaluated yet!")
        x_path = [self.end.x]
        y_path = [self.end.y]
        current_point = self.end
        while True:
            new_parent = self.map[current_point.y, current_point.x].par
            x_path.append(new_parent.x)
            y_path.append(new_parent.y)
            if new_parent.x == self.start.x and new_parent.y == self.start.y:
                break;
            current_point = new_parent
        return x_path, y_path


