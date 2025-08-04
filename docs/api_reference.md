# API Reference - Rubik's Cube Solver

## AeroHack 2025 - Collins Aerospace
**Author:** Ullas Vandana

---

## Table of Contents

1. [Core Classes](#core-classes)
2. [Algorithm Classes](#algorithm-classes)
3. [UI Classes](#ui-classes)
4. [Utility Functions](#utility-functions)
5. [Examples](#examples)
6. [Error Handling](#error-handling)

---

## Core Classes

### RubikCube

The main cube representation and manipulation class.

#### Constructor

```python
RubikCube(state: Optional[np.ndarray] = None)
```

**Parameters:**
- `state` (optional): 54-element numpy array representing cube state
- If None, creates a solved cube

**Example:**
```python
# Create solved cube
cube = RubikCube()

# Create from existing state
custom_state = np.arange(54)
cube = RubikCube(custom_state)
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `state` | `np.ndarray` | 54-element array of cube state |
| `move_history` | `List[str]` | List of executed moves |

#### Methods

##### Core Operations

```python
execute_move(move: str) -> None
```
Execute a single move on the cube.

**Parameters:**
- `move`: Standard notation move (e.g., 'U', 'R\'', 'F2')

**Raises:**
- `ValueError`: If move is invalid

**Example:**
```python
cube.execute_move('U')
cube.execute_move('R\'')
```

```python
execute_sequence(moves: List[str]) -> None
```
Execute a sequence of moves.

**Parameters:**
- `moves`: List of moves in standard notation

**Example:**
```python
cube.execute_sequence(['R', 'U', 'R\'', 'U\''])
```

```python
scramble(num_moves: int = 20, seed: Optional[int] = None) -> List[str]
```
Scramble the cube with random moves.

**Parameters:**
- `num_moves`: Number of scramble moves (default: 20)
- `seed`: Random seed for reproducible scrambles

**Returns:**
- List of scramble moves executed

**Example:**
```python
scramble_moves = cube.scramble(15, seed=42)
print(f"Scramble: {' '.join(scramble_moves)}")
```

##### State Management

```python
is_solved() -> bool
```
Check if the cube is in solved state.

**Returns:**
- `True` if solved, `False` otherwise

```python
copy() -> 'RubikCube'
```
Create a deep copy of the cube.

**Returns:**
- New RubikCube instance with identical state

```python
reset() -> None
```
Reset cube to solved state.

```python
get_state_string() -> str
```
Get string representation of cube state for hashing.

**Returns:**
- 54-character string representing state

##### Face Operations

```python
get_face(face_idx: int) -> np.ndarray
```
Get a specific face as 3×3 array.

**Parameters:**
- `face_idx`: Face index (0-5)

**Returns:**
- 3×3 numpy array representing the face

**Face Indices:**
- 0: Front (White)
- 1: Right (Red)
- 2: Back (Blue)
- 3: Left (Orange)
- 4: Up (Green)
- 5: Down (Yellow)

```python
set_face(face_idx: int, face_data: np.ndarray) -> None
```
Set a specific face from 3×3 array.

**Parameters:**
- `face_idx`: Face index (0-5)
- `face_data`: 3×3 numpy array

##### Utility Methods

```python
get_move_count() -> int
```
Get number of moves executed.

**Returns:**
- Number of moves in move history

---

### MoveEngine

Handles all move operations and transformations.

#### Constructor

```python
MoveEngine()
```

#### Methods

```python
get_all_moves() -> List[str]
```
Get list of all valid moves.

**Returns:**
- List of 18 standard moves

```python
is_valid_move(move: str) -> bool
```
Check if a move is valid.

**Parameters:**
- `move`: Move string to validate

**Returns:**
- `True` if valid, `False` otherwise

```python
apply_move(state: np.ndarray, move: str) -> np.ndarray
```
Apply move to state and return new state.

**Parameters:**
- `state`: Current cube state
- `move`: Move to apply

**Returns:**
- New state after move application

---

## Algorithm Classes

### AStarSolver

Main A* search algorithm implementation.

#### Constructor

```python
AStarSolver(max_depth: int = 25, timeout: float = 60.0)
```

**Parameters:**
- `max_depth`: Maximum search depth
- `timeout`: Maximum solve time in seconds

#### Methods

```python
solve(cube: RubikCube, heuristic_type: str = 'corner_edge') -> Optional[List[str]]
```
Solve the cube using A* algorithm.

**Parameters:**
- `cube`: Cube to solve
- `heuristic_type`: Heuristic function ('manhattan', 'corner_edge', 'combined')

**Returns:**
- List of moves to solve cube, or None if no solution found

**Example:**
```python
solver = AStarSolver(max_depth=20, timeout=30)
solution = solver.solve(cube, heuristic_type='corner_edge')

if solution:
    print(f"Solution: {' '.join(solution)}")
    cube.execute_sequence(solution)
    print(f"Solved: {cube.is_solved()}")
```

```python
solve_iterative_deepening(cube: RubikCube) -> Optional[List[str]]
```
Fallback iterative deepening search.

**Parameters:**
- `cube`: Cube to solve

**Returns:**
- Solution moves or None

```python
get_statistics() -> SearchStatistics
```
Get search statistics from last solve attempt.

**Returns:**
- SearchStatistics object with performance data

---

### Heuristics

Collection of heuristic functions for A* search.

#### Constructor

```python
Heuristics()
```

#### Methods

```python
manhattan_distance(cube: RubikCube) -> int
```
Basic Manhattan distance heuristic.

```python
corner_edge_heuristic(cube: RubikCube) -> int
```
Advanced corner-edge based heuristic.

```python
combined_heuristic(cube: RubikCube) -> int
```
Combined multiple heuristics.

```python
estimate_moves_to_solve(cube: RubikCube) -> int
```
Primary heuristic used by solver.

---

## UI Classes

### ConsoleInterface

Interactive console interface for the solver.

#### Constructor

```python
ConsoleInterface(cube: RubikCube, solver: AStarSolver)
```

**Parameters:**
- `cube`: Cube instance to operate on
- `solver`: Solver instance to use

#### Methods

```python
run() -> None
```
Start the interactive interface main loop.

**Example:**
```python
cube = RubikCube()
solver = AStarSolver()
interface = ConsoleInterface(cube, solver)
interface.run()
```

---

### CubeVisualizer

Visualization capabilities for cube states.

#### Constructor

```python
CubeVisualizer()
```

#### Methods

```python
display_ascii_art(cube: RubikCube) -> str
```
Generate ASCII art representation.

**Parameters:**
- `cube`: Cube to visualize

**Returns:**
- ASCII art string

```python
display_detailed_console(cube: RubikCube) -> None
```
Display detailed console representation.

```python
display_2d_net(cube: RubikCube, title: str = "Rubik's Cube State") -> None
```
Display 2D net using matplotlib.

```python
save_state_image(cube: RubikCube, filename: str, title: str = None) -> None
```
Save cube state as image file.

---

## Utility Functions

### MoveOptimizer

Optimizes move sequences by removing redundancies.

#### Constructor

```python
MoveOptimizer()
```

#### Methods

```python
optimize_sequence(moves: List[str]) -> List[str]
```
Optimize a move sequence.

**Parameters:**
- `moves`: List of moves to optimize

**Returns:**
- Optimized move sequence

**Example:**
```python
optimizer = MoveOptimizer()
original = ['U', 'U', 'U', 'R', 'R\'']
optimized = optimizer.optimize_sequence(original)
print(f"Original: {original}")
print(f"Optimized: {optimized}")
```

### Utility Functions

```python
format_move_sequence(moves: List[str], line_length: int = 50) -> str
```
Format move sequence for display.

**Parameters:**
- `moves`: List of moves
- `line_length`: Maximum line length

**Returns:**
- Formatted string with line breaks

```python
analyze_move_sequence(moves: List[str]) -> Dict[str, int]
```
Analyze move sequence statistics.

**Parameters:**
- `moves`: List of moves to analyze

**Returns:**
- Dictionary with analysis results

**Example:**
```python
moves = ['R', 'U', 'R\'', 'U\'']
analysis = analyze_move_sequence(moves)
print(f"Total moves: {analysis['total_moves']}")
print(f"Face distribution: {analysis['face_distribution']}")
```

### SearchStatistics

Data class for search performance statistics.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `nodes_explored` | `int` | Number of nodes explored |
| `solution_found` | `bool` | Whether solution was found |
| `solution_length` | `int` | Length of solution |
| `solve_time` | `float` | Time taken to solve |

#### Methods

```python
reset() -> None
```
Reset all statistics to defaults.

---

## Examples

### Basic Usage

```python
from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver

# Create and scramble cube
cube = RubikCube()
cube.scramble(10)

# Solve cube
solver = AStarSolver(max_depth=15, timeout=30)
solution = solver.solve(cube)

if solution:
    print(f"Solution found: {len(solution)} moves")
    cube.execute_sequence(solution)
    print(f"Cube solved: {cube.is_solved()}")
```

### Advanced Usage

```python
from src.algorithms.utils import MoveOptimizer, format_move_sequence

# Create complex scramble
cube = RubikCube()
scramble = ['R', 'U', 'R\'', 'F\'', 'R', 'U\'', 'R\'', 'U\'', 'R\'', 'F', 'R2', 'U\'', 'R\'']
cube.execute_sequence(scramble)

# Solve with different heuristics
solver = AStarSolver(max_depth=20, timeout=45)

for heuristic in ['manhattan', 'corner_edge', 'combined']:
    test_cube = cube.copy()
    solution = solver.solve(test_cube, heuristic_type=heuristic)
    
    if solution:
        optimizer = MoveOptimizer()
        optimized = optimizer.optimize_sequence(solution)
        
        print(f"{heuristic}: {len(optimized)} moves")
        print(format_move_sequence(optimized))
```

### Performance Testing

```python
import time

# Performance test
scramble_lengths = [5, 10, 15, 20]
results = []

for length in scramble_lengths:
    cube = RubikCube()
    cube.scramble(length, seed=42)
    
    solver = AStarSolver(max_depth=25, timeout=60)
    
    start_time = time.time()
    solution = solver.solve(cube)
    solve_time = time.time() - start_time
    
    stats = solver.get_statistics()
    
    results.append({
        'scramble_length': length,
        'solution_length': len(solution) if solution else None,
        'solve_time': solve_time,
        'nodes_explored': stats.nodes_explored,
        'success': solution is not None
    })

# Print results
for result in results:
    print(f"Length {result['scramble_length']}: {result}")
```

---

## Error Handling

### Common Exceptions

| Exception | Cause | Solution |
|-----------|-------|----------|
| `ValueError` | Invalid move notation | Use standard notation (U, R', F2, etc.) |
| `ValueError` | Invalid cube state | Ensure 54-element array with valid colors |
| `ValueError` | Invalid face index | Use face indices 0-5 |
| `ValueError` | Invalid heuristic type | Use 'manhattan', 'corner_edge', or 'combined' |

### Example Error Handling

```python
try:
    cube = RubikCube()
    cube.execute_move('X')  # Invalid move
except ValueError as e:
    print(f"Invalid move: {e}")

try:
    solver = AStarSolver()
    solution = solver.solve(cube, heuristic_type='invalid')
except ValueError as e:
    print(f"Invalid heuristic: {e}")
```

---

## Notes

- All move notation follows standard Rubik's Cube conventions
- Cube state arrays use integers 0-5 representing colors
- Search algorithms are configurable for different performance profiles
- All classes are designed to be thread-safe for concurrent use
- Memory usage scales with search depth and complexity

For more examples and advanced usage, see the `examples/` directory in the project repository.