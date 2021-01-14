from collections import deque
import itertools
from heapq import heappush, heappop, heapify
import timeit
import resource
import sys
import math


class Board(object):
    
    def __init__(self, config, n, cost=0, parent=None, action="Initial"):
        
        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.dimension = n

        self.config = config
        
        self.parent = parent
        
        self.action = action
        
        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n
                
                self.blank_index = i

                break


    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)
            
            
    def configMap(self):
        
        return tuple(self.config)
            
            
    def move_left(self):
        
        if self.blank_col == 0:

            return None

        else:

            target = self.blank_index - 1

            new_config = list(self.config)

            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]

            return Board(tuple(new_config), self.n, cost=self.cost + 1, parent=self, action="Left")
        

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            target = self.blank_index + 1

            new_config = list(self.config)

            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]

            return Board(tuple(new_config), self.n, cost=self.cost + 1, parent=self, action="Right")
        

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            target = self.blank_index - self.n

            new_config = list(self.config)

            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]

            return Board(tuple(new_config), self.n, cost=self.cost + 1, parent=self, action="Up")
        

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            target = self.blank_index + self.n

            new_config = list(self.config)

            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]

            return Board(tuple(new_config), self.n, cost=self.cost + 1, parent=self, action="Down")
        

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR
        
        children = []

        up_child = self.move_up()

        if up_child is not None:

            children.append(up_child)

        down_child = self.move_down()

        if down_child is not None:

            children.append(down_child)

        left_child = self.move_left()

        if left_child is not None:

            children.append(left_child)

        right_child = self.move_right()

        if right_child is not None:

            children.append(right_child)

        return children
    


nodes_expanded = 0
max_search_depth = 0


def bfs_search(initial_board):

    """BFS search"""
    queue = deque()
    frontier = set()
    visitedNodes = set() #visited nodes
    
    queue.append(initial_board)
    frontier.add(initial_board.configMap())
    
    global nodes_expanded, max_search_depth
    
    while queue:
        
        board = queue.popleft()
        
        if test_goal(board):
            return board
        
        children = board.expand()
        nodes_expanded += 1
        
        for child in children:
            if child.configMap() not in frontier:
                queue.append(child)
                frontier.add(child.configMap())
                
                if(child.cost > max_search_depth):
                    max_search_depth = child.cost
        
    return None
            
        


def dfs_search(initial_board):

    """DFS search"""
    
    stack = deque()
    frontier = set()
    
    stack.append(initial_board)
    frontier.add(initial_board.configMap())
    
    global nodes_expanded, max_search_depth
    
    while stack:
    
        board = stack.pop()
                
        if test_goal(board):
            return board
        
        children = reversed(board.expand())
        nodes_expanded += 1
        
        for child in children:
            if child.configMap() not in frontier:
                stack.append(child)
                frontier.add(child.configMap())
                
                if(child.cost > max_search_depth):
                    max_search_depth = child.cost
        
    return None


def A_star_search(initial_board):

    """A* search"""
    
    counter = itertools.count() 
    pq = []
    entry_finder = {}
    explored = set()
    
    priority = get_priority(initial_board)
    
    entry = [priority, -1, initial_board]
    
    entry_finder[initial_board.configMap()] = entry
    
    heappush(pq, entry)
    
    global nodes_expanded, max_search_depth
    
    while pq:
        
        state = heappop(pq)
        
        board = state[2]
        
        explored.add(board.configMap())
        entry_finder.pop(board.configMap(), None)
        
        if test_goal(board):
            return board
        
        children = board.expand()
        nodes_expanded += 1
        
        for child in children:
            
            priority = get_priority(child)
            
            count = next(counter)
            
            entry = [priority, count, child]
            
            if child.configMap() not in explored and child.configMap() not in entry_finder:
                
                heappush(pq, entry)
                
                entry_finder[child.configMap()] = entry
                
                
            elif child.configMap() in entry_finder and priority < get_priority(entry_finder[child.configMap()][2]):
                
                old_entry = entry_finder[child.configMap()]
                
                heap_index = pq.index(old_entry)
                
                pq[int(heap_index)] = entry
                
                entry_finder[child.configMap()] = entry
                
                heapify(pq)
            
            if(child.cost > max_search_depth):
                max_search_depth = child.cost
                    
    return None


def manhattan_dist(board):
    
    """Manhattan Distance - Heuristic score"""
    
    sum = 0
    for i, val in enumerate(board.config):
        if val != 0:
            sum += abs(val//board.n - i//board.n) + abs(val%board.n - i%board.n)
    
    return sum

def get_priority(board):
    
    """ f-score = g(n) + h(n) """
    
    return manhattan_dist(board) + board.cost


goal = (0,1,2,3,4,5,6,7,8)

goalHash = hash(goal)

def test_goal(board):
    
    """test the state is the goal state or not"""
    
    config = tuple(board.config)
    
    if(hash(config) == goalHash):
        return True
    else: 
        return False
    
    
def calculate_path(board):
    
    """Calculate the path after finding the goal state"""
    
    path_to_goal = []
    
    while(board.action != "Initial"):
        path_to_goal.insert(0,board.action)
        board = board.parent
    
    return path_to_goal


def writeOutput(board, runtime):
    
    file = open('output.txt', 'w')
    file.write('path_to_goal: ' + str(calculate_path(board)))
    file.write('\ncost_of_path: ' + str(board.cost))
    file.write('\nnodes_expanded: ' + str(nodes_expanded))
    file.write('\nsearch_depth: ' + str(board.cost))
    file.write('\nmax_search_depth: ' + str(max_search_depth))
    file.write('\nrunning_time: ' + format(runtime, '.8f'))
    file.write('\nmax_ram_usage: ' + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.8f'))    
    file.close()


def main():

    sm = sys.argv[1].lower()

    initial_config = sys.argv[2].split(",")
    
    initial_config = tuple(map(int, initial_config))

    size = int(math.sqrt(len(initial_config)))

    initial_board = Board(initial_config, size)

    if sm == "bfs":
        
        start = timeit.default_timer()
        answer_node = bfs_search(initial_board)
        end = timeit.default_timer()

    elif sm == "dfs":
        
        start = timeit.default_timer()
        answer_node = dfs_search(initial_board)
        end = timeit.default_timer()

    elif sm == "ast":

        start = timeit.default_timer()
        answer_node = A_star_search(initial_board)
        end = timeit.default_timer()
        

    else:

        print("Enter valid command arguments !")
        return
    
    writeOutput(answer_node, end - start)

if __name__ == '__main__':

    main()