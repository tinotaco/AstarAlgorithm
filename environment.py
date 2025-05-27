import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

class Environment:
    def __init__(self, rows, columns):
        self.environment = np.full((rows, columns), 0)
        self.rows = rows
        self.columns = columns
        self.startpos = Point(0, 0)

    def plotenvironment(self):
        fig, ax = plt.subplots(figsize= (10,10))

        # Define the color map
        
        cmap = LinearSegmentedColormap.from_list('custom_gray', ['white', 'gray', 'black'])
        cax = ax.imshow(np.flipud(self.environment), cmap=cmap, extent=[0, self.columns, 0, self.rows], interpolation='nearest', vmin=0, vmax=1)

        plt.text(self.startpos.x, self.startpos.y, 'X', color='red',
         ha='center', va='center', fontsize=14, fontweight='bold')

        plt.text(self.endpos.x, self.endpos.y, 'O', color='green',
            ha='center', va='center', fontsize=14, fontweight ='bold')

        #ax.set_xticks(np.arange(0, self.x_dist+1, 1))
        #ax.set_yticks(np.arange(0, self.y_dist+1, 1))

        plt.title('2D Grid Visualization')
        plt.xlabel('Column Index')
        plt.ylabel('Row Index')
        plt.colorbar(cax, ax=ax, ticks=[0,1], label='Occupancy')

        plt.show()
    
    def addblockrow(self, xStart, yStart, xAmt):
        for it in range(xStart, xStart + xAmt + 1):
            self.environment[yStart, it] = 1
    
    def addblockcolumn(self, xStart, yStart, yAmt):
        for it in range(yStart, yStart + yAmt + 1):
            self.environment[it, xStart] = 1
    
    def setstartpos(self, x, y):
        self.startpos = Point(x, y)
    
    def endpos(self, x, y):
        self.endpos = Point(x, y)
    