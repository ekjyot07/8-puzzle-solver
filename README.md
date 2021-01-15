# 8-puzzle-solver

Implemented **BFS**, **DFS**, and **A\* algorithms** to solve the 8-puzzle game.

**The problem**: The 8-puzzle is a sliding puzzle that is played on a 3-by-3 grid with 8 square tiles labeled 1 through 8, plus a blank square. The goal is to rearrange the tiles so that they are in row-major order, using as few moves as possible. You are permitted to slide tiles either horizontally or vertically into the blank square. The following diagram shows a sequence of moves from an initial board (left) to the goal board (right).

<p align='center'>
<img width="75%" height="75%" src="https://www.cs.princeton.edu/courses/archive/spring18/cos226/assignments/8puzzle/4moves.png" />
</p>

## Usage
```
python3 driver.py <method> <board>

Methods:
bfs (Breadth-First Search)
dfs (Depth-First Search)
ast (A-Star Search)
```

## Results
```
$ python3 driver.py ast 8,6,4,2,1,3,5,7,0

path_to_goal: ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Left']
cost_of_path: 26
nodes_expanded: 1660
search_depth: 26
max_search_depth: 26
running_time: 0.05156748
max_ram_usage: 10.40400000
```


