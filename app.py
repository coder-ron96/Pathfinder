# app.py
import curses
from curses import wrapper
import queue
import time

from flask import Flask, jsonify
from flask_cors import CORS  # This allows cross-origin requests from your HTML page

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the maze layout
maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "X"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " "],
    ["#", "#", " ", " ", " ", "#", " ", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", " ", "#"],
    ["#", "#", " ", " ", " ", " ", " ", "#", "#"],
    [" ", "#", "#", " ", "#", "#", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", " ", " ", "#", " "],
    ["#", "#", " ", "#", " ", "#", " ", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "O", "#", " ", "#", " ", "#", " ", "#"]
]

def print_maze(maze, stdscr, path=[]):
    curses.curs_set(0)  # Hide the cursor
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j, "X", RED)
            else:
                stdscr.addstr(i, j, value, BLUE)

def find_start(maze, start):
    """Find the starting position 'O' in the maze."""
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

def find_path(maze, stdscr):
    """Find the shortest path from 'O' to 'X' using BFS."""
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    if start_pos is None:
        raise ValueError("Start position not found in the maze")

    # Initialize the queue with the starting position and path
    q = queue.Queue()
    q.put((start_pos, [start_pos]))  # Each entry in the queue is (position, path)

    visited = set([start_pos])

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        # Check if the end has been reached
        if maze[row][col] == end:
            stdscr.getch()  # Pause to view the path
            return path

        # Explore neighbors
        for neighbor in find_neighbors(maze, row, col):
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            # Append neighbor to path and mark as visited
            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)

def find_neighbors(maze, row, col):
    """Find all valid neighbors (up, down, left, right) that are not walls."""
    neighbors = []

    if row > 0:  # Up
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # Down
        neighbors.append((row + 1, col))
    if col > 0:  # Left
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # Right
        neighbors.append((row, col + 1))

    return neighbors

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # Start the pathfinding
    find_path(maze, stdscr)
    
    # Wait for a key press to keep the window open
    stdscr.getch()

wrapper(main)

@app.route('/run-pathfinder', methods=['GET'])
def run_pathfinder():
    result = "Pathfinder result goes here"  # Replace with your actual Pathfinder logic if needed
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
