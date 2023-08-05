#!/usr/bin/env python

"""The cyclone module (the only module).
Classes:
    CyclePower: represent powers of a cycle graph
        get_coord
        get_index
        add
        remove
        hasPoint
        size
        toString
Functions:
    create_starting_set: 
        creates a naive starting independent set in
        a cycle graph of the given dimensions
    count_neighbors:
        count the number of neighbors the given point has
        in the CyclePower instance
"""

import numpy as np
from random import randint

class CyclePower:
    """Class used to represent a power of a cycle graph.
    
    Dependencies
    ------------
    numpy and random
    
    Attributes
    ----------
    cycle: int
        number to indicate the cycle of the base graph 
        (i.e., the modulus of each coordinate).
    power: int
        number to indicate the power of the Cartesian
        product (i.e., the number of coordinates/dimensions).
    points: array of shorts
        array to keep track of what points are in the graph.
        the index indicates the point number, and a 1 at that
        position indicates that the point is in the graph
        (0 if not in the graph).
        
    Methods
    -------
    get_coord(index)
        converts an array index to its coordinate representation
    get_index(coord)
        converts a coordinate to the corresponding array index
    add(point)
        adds a point to the graph
    remove(point)
        removes a point from the graph
    hasPoint(point)
        checks if the graph contains the given point
    size
        returns the size of the graph (number of points)
    toString
        returns an array of vertices contained in the graph
    """
        
    def __init__(self, cycle, power):
        """
        Parameters
        ----------
        cycle: int
            number to indicate the cycle of the base graph 
            (i.e., the modulus of each coordinate).
        power: int
            number to indicate the power of the Cartesian
            product (i.e., the number of coordinates/dimensions).
        """
        self.cycle = cycle
        self.power = power
        self.points = np.zeros(shape=np.power(cycle,power), order='C', dtype=np.short) 
        
    def get_coord(self, num):
        """Given an index, returns the corresponding coordinate
        representation.

        :param num: Index of a point.
        :return: Numpy array. The coordinate of the point.
        """
        coord = np.zeros(shape=self.power, order='C', dtype=np.short)

        for i in range(self.power):
            index=self.power-i-1
            divisor=np.power(self.cycle, index)
            coord[index]=num/divisor
            num=num%divisor
        return coord

    def get_index(self, coord):
        """Opposite of `get_coord`. Given a coordinate representation 
        of a point, returns the corresponding index in the array of
        the graph.

        :param coord: Numpy array. The coordinate of a point.
        :return: Number. The index of the point in the array
        representation.
        """
        num = 0

        for index in range(len(coord)): # index goes from 0 to power-1
            num = num+(np.power(self.cycle,index)*coord[index])
        return num

    def add(self, point_num):
        """Add a point to a graph.

        :param point_num: Index of the point to be added.
        :return: None.
        """
        self.points[point_num] = 1

    def remove(self, point_num):
        """Remove a point from a graph.

        :param point_num: Index of the point to be removed.
        :return: None.
        """
        self.points[point_num] = 0

    def hasPoint(self, point_num):
        """Check if a point is in the graph.

        :param point_num: Index of the point to check.
        :return: Boolean. True if in the graph, False if not.
        """
        if(self.points[point_num] == 1):
            return True
        return False

    def size(self):
        """Calculates the size (number of vertices) of a graph.

        :return: Number. Number of points in the graph.
        """
        count = 0
        for i in self.points:
            if(i==1):
                count+=1
        return count

    def toString(self):
        """Print the vertices of a graph.

        :return: Array. List of vertices in the graph represented as
        coordinates.
        """

        pointList = [np.empty(shape=(1,self.power))]
        for i in range(len(points)):
            if(points[i]==1):
                pointList.append(get_coord(i))
        return np.asarray(pointList)
        
def create_starting_graph(cycle, power):
    """Creates a naive starting independent set.

    :param cycle: number to indicate the cycle of the base graph 
    (i.e., the modulus of each coordinate).
    :param power: number to indicate the power of the Cartesian
    product (i.e., the number of coordinates/dimensions).
    :return: instance of class CyclePower.
    """
    cp = CyclePower(cycle, power)
    
    cp.add(cp.get_index(np.ones(shape=cp.power, dtype=np.short)))
    for num in range(1, np.power(3, cp.power)):
        count = np.zeros(shape=cp.power, order='C', dtype=np.short)
        for i in range(cp.power):
            index=cp.power-i-1
            divisor=np.power(3, index)
            count[index]=num/divisor
            num=num%divisor
        special = count
        for index in range(len(count)):
            if count[index] == 0:
                special[index] = 1
            elif count[index] == 1:
                special[index] = 3
            else:
                special[index] = 5
        cp.add(cp.get_index(special)) 
        
    return cp

def count_neighbors(point, cp):
    """Count the number of neighbors a point has in the set.
    Does not include the point intself.
    
    A neighbor is the point's coordinate [a0, a1, ..., an] 
    + a vector [v0, v1, ..., vn]
    
    The addition vector is calculated as follows:
    v_j = (count_j + 1)/2 * (-1)^count_j

    :param point: The point, represented as an index that will
     be converted into a coordinate.
    :param cp: instance of class CyclePower.
    :return: int, numpy array of coordinates. The number of 
    neighbors and the set of neighbors.
    """
    coord = cp.get_coord(point)

    # keep count of num neighbors and a set of neighbors
    num_neighb = 0
    set_neighb = []
    
    # count up in ternary from 1 to 3^power-1
    # [0, 0, ..., 1], [0, 0, ..., 2], ...
    for num in range(1, np.power(3, cp.power)):
        count = np.zeros(shape=cp.power, order='C', dtype=np.short)
        for i in range(cp.power):
            index=cp.power-i-1
            divisor=np.power(3, index)

            count[index]=num/divisor
            num=num%divisor
        
        # addition vector
        vect = np.zeros(shape=cp.power, order='C', dtype=np.short)
        for i in range(cp.power):
            vect[i] = ((count[i]+1)/2) * np.power(-1, count[i])
        
        neighb = (coord + vect) % cp.cycle
        
        # if neighbor is in the set
        if(cp.hasPoint(cp.get_index(neighb)) and cp.get_index(neighb) != point):
            num_neighb+=1
            set_neighb.append(neighb)
    
    return num_neighb, set_neighb

# return 0, 1, or 2
# TODO: break when find second neighbor