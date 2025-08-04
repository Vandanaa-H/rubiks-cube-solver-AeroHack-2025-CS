# User Guide - Rubik's Cube Solver

## AeroHack 2025 - Collins Aerospace
**Author:** Vandana

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Interactive Interface](#interactive-interface)
5. [Command Line Usage](#command-line-usage)
6. [Configuration Options](#configuration-options)
7. [Understanding Results](#understanding-results)
8. [Tips and Best Practices](#tips-and-best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Getting Started

Welcome to the Rubik's Cube Solver! This application uses advanced A* search algorithms to solve Rubik's Cube puzzles optimally. Whether you're a beginner learning about algorithms or an expert looking for efficient solutions, this solver provides both educational value and practical functionality.

### What You'll Learn
- How A* search algorithms work
- Rubik's Cube notation and mechanics
- Heuristic function design
- Performance optimization techniques

### Prerequisites
- Basic understanding of Rubik's Cube notation
- Python 3.8 or higher
- Familiarity with command line interfaces (helpful but not required)

---

## Installation

### 1. System Requirements

**Minimum Requirements:**
- Python 3.8+
- 4GB RAM
- 100MB disk space

**Recommended:**
- Python 3.9+
- 8GB RAM
- SSD storage

### 2. Dependencies Installation

```bash
# Navigate to project directory
cd c:\Users\ullas\Desktop\Vandana

# Install required packages
pip install -r requirements.txt
```

**Required Packages:**
- `numpy`: Numerical computations
- `matplotlib`: Visualization
- `colorama`: Colored console output
- `pytest`: Testing framework

### 3. Verify Installation

```bash
# Run basic test
python -c "from src.core.cube import RubikCube; print('Installation successful!')"

# Run full verification
python main.py
```

---

## Basic Usage

### Quick Start Example

```python
from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver

# Create a new cube
cube = RubikCube()
print(f"Cube is solved: {cube.is_solved()}")

# Scramble the cube
scramble_moves = cube.scramble(10)
print(f"Scrambled with: {' '.join(scramble_moves)}")

# Solve the cube
solver = AStarSolver()
solution = solver.solve(cube)

if solution:
    print(f"Solution: {' '.join(solution)}")
    cube.execute_sequence(solution)
    print(f"Cube is now solved: {cube.is_solved()}")
```

### Understanding Cube Notation

The solver uses standard Rubik's Cube notation:

| Notation | Face | Direction |
|----------|------|-----------|
| U | Up (Top) | Clockwise 90° |
| U' | Up (Top) | Counterclockwise 90° |
| U2 | Up (Top) | 180° |
| D | Down (Bottom) | Clockwise 90° |
| D' | Down (Bottom) | Counterclockwise 90° |
| D2 | Down (Bottom) | 180° |
| R | Right | Clockwise 90° |
| R' | Right | Counterclockwise 90° |
| R2 | Right | 180° |
| L | Left | Clockwise 90° |
| L' | Left | Counterclockwise 90° |
| L2 | Left | 180° |
| F | Front | Clockwise 90° |
| F' | Front | Counterclockwise 90° |
| F2 | Front | 180° |
| B | Back | Clockwise 90° |
| B' | Back | Counterclockwise 90° |
| B2 | Back | 180° |

### Color Scheme

The default color scheme follows standard conventions:
- **White**: Front face (when solved)
- **Red**: Right face
- **Blue**: Back face
- **Orange**: Left face
- **Green**: Up face
- **Yellow**: Down face

---

## Interactive Interface

### Starting the Interface

```bash
python main.py
```

This launches the interactive console interface with a beautiful menu system.

### Main Menu Options

#### 1. View Current Cube State
- Shows current cube configuration
- Displays move history
- Shows ASCII representation

**Example Output:**
```
═══ CURRENT CUBE STATE ═══

Cube Status: SOLVED ✓
Moves Made: 0

Cube Visualization:
      G G G
      G G G
      G G G

O O O W W W R R R B B B
O O O W W W R R R B B B
O O O W W W R R R B B B

      Y Y Y
      Y Y Y
      Y Y Y
```

#### 2. Scramble Cube
- Interactive scrambling with custom move count
- Shows scramble sequence
- Displays resulting cube state

**Usage:**
1. Select option 2
2. Enter number of moves (default: 20)
3. View scramble sequence and result

#### 3. Solve Cube
- Attempts to solve current cube state
- Shows search progress
- Displays solution and statistics

**Process:**
1. Algorithm analyzes cube state
2. A* search finds optimal solution
3. Results displayed with timing information
4. Option to apply solution to cube

#### 4. Execute Manual Moves
- Input custom move sequences
- Real-time cube state updates
- Move validation and error checking

**Supported Formats:**
```
Single moves: U
Multiple moves: U R U' R'
Complex sequences: R U R' F' R U R' U' R' F R2 U' R'
```

#### 5. Reset to Solved State
- Instantly returns cube to solved state
- Clears move history
- Confirmation prompt for safety

#### 6. Load Scramble from File
- Load predefined scrambles
- Categories: Easy, Medium, Hard
- Custom file support

#### 7. Performance Test
- Benchmark solver performance
- Multiple test cases
- Statistical analysis

#### 8. Solver Settings
- Adjust search parameters
- Timeout configuration
- Depth limits

#### 9. Help & Instructions
- Detailed notation guide
- Algorithm information
- Usage tips

---

## Command Line Usage

### Direct Solving

```bash
# Solve with custom scramble
python -c "
from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver

cube = RubikCube()
cube.execute_sequence(['U', 'R', 'U\'', 'R\''])

solver = AStarSolver()
solution = solver.solve(cube)
print(' '.join(solution) if solution else 'No solution found')
"
```

### Batch Processing

```bash
# Process multiple scrambles
python examples/performance_test.py
```

### Custom Scripts

Create custom solving scripts:

```python
# solve_custom.py
import sys
from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver

def solve_scramble(scramble_str):
    cube = RubikCube()
    moves = scramble_str.split()
    cube.execute_sequence(moves)
    
    solver = AStarSolver(max_depth=20, timeout=30)
    solution = solver.solve(cube)
    
    return solution

if __name__ == "__main__":
    scramble = sys.argv[1] if len(sys.argv) > 1 else "U R U' R'"
    solution = solve_scramble(scramble)
    
    if solution:
        print(f"Solution: {' '.join(solution)}")
    else:
        print("No solution found")
```

Usage:
```bash
python solve_custom.py "R U R' F' R U R' U' R' F R2 U' R'"
```

---

## Configuration Options

### Solver Parameters

#### Max Depth
Controls how deep the search algorithm will go.

```python
solver = AStarSolver(max_depth=25)  # Default: 25
```

**Guidelines:**
- **5-10**: Very fast, basic scrambles only
- **15-20**: Good balance for most scrambles
- **25-30**: Thorough search, slower but comprehensive
- **30+**: Research/academic use, very slow

#### Timeout
Maximum time to spend searching (in seconds).

```python
solver = AStarSolver(timeout=60.0)  # Default: 60 seconds
```

**Guidelines:**
- **10-15s**: Quick interactive use
- **30-60s**: Standard desktop use
- **120s+**: Complex scrambles, batch processing

#### Heuristic Function
Choose the heuristic function for A* search.

```python
solution = solver.solve(cube, heuristic_type='corner_edge')
```

**Options:**
- `'manhattan'`: Basic distance heuristic (fastest)
- `'corner_edge'`: Advanced piece-based heuristic (recommended)
- `'combined'`: Multi-heuristic approach (most accurate)

### Performance Tuning

#### For Speed (Interactive Use)
```python
solver = AStarSolver(
    max_depth=15,
    timeout=20,
)
solution = solver.solve(cube, heuristic_type='manhattan')
```

#### For Quality (Best Solutions)
```python
solver = AStarSolver(
    max_depth=30,
    timeout=120,
)
solution = solver.solve(cube, heuristic_type='combined')
```

#### For Research (Comprehensive)
```python
solver = AStarSolver(
    max_depth=40,
    timeout=300,
)
solution = solver.solve(cube, heuristic_type='corner_edge')
```

---

## Understanding Results

### Solution Output

When a solution is found, you'll see:

```
✅ SOLUTION FOUND!
Solution length: 12 moves
Solution sequence: R U R' F' R U R' U' R' F R2 U' R'

Search Statistics:
  Nodes explored: 1,247
  Solve time: 3.45s
  Solution length: 12
  Success rate: 100%
```

### Statistics Explained

| Metric | Description | Good Values |
|--------|-------------|-------------|
| **Solution Length** | Number of moves in solution | < 25 moves |
| **Solve Time** | Time taken to find solution | < 30 seconds |
| **Nodes Explored** | Search space explored | Depends on scramble |
| **Success Rate** | Whether solution was found | 100% |

### Quality Assessment

#### Excellent Results
- Solution length ≤ scramble length + 5
- Solve time < 10 seconds
- Nodes explored < 10,000

#### Good Results
- Solution length ≤ scramble length × 1.5
- Solve time < 30 seconds
- Solution found within limits

#### Acceptable Results
- Solution found (any length)
- Solve time < timeout limit
- Functional for intended use

### Common Result Patterns

#### Simple Scrambles (1-8 moves)
```
Scramble: U R U' R'
Solution: R U R' U'
Analysis: Near-optimal, very fast
```

#### Medium Scrambles (9-15 moves)
```
Scramble: R U R' F' R U R' U' R' F R2 U' R'
Solution: R U2 R' F' R U R' U' R' F R2 U' R' U
Analysis: Good length, reasonable time
```

#### Complex Scrambles (16+ moves)
```
Scramble: [20 move scramble]
Solution: [25-35 move solution]
Analysis: May timeout, use higher limits
```

---

## Tips and Best Practices

### For Beginners

1. **Start Simple**
   - Begin with 1-5 move scrambles
   - Learn the notation gradually
   - Use default solver settings

2. **Use the Interactive Interface**
   - More user-friendly than command line
   - Built-in help and guidance
   - Visual feedback

3. **Study the Solutions**
   - Analyze why certain moves work
   - Compare different solving approaches
   - Learn common algorithms

### For Intermediate Users

1. **Experiment with Settings**
   - Try different heuristic functions
   - Adjust depth and timeout limits
   - Compare performance trade-offs

2. **Use Performance Testing**
   - Benchmark your settings
   - Identify optimal configurations
   - Track improvement over time

3. **Learn Advanced Features**
   - Move optimization utilities
   - Batch processing capabilities
   - Custom scramble creation

### For Advanced Users

1. **Customize Algorithms**
   - Modify heuristic functions
   - Implement new search strategies
   - Optimize for specific scenarios

2. **Integration Projects**
   - Use as library in larger projects
   - Connect to robot controllers
   - Build web interfaces

3. **Research Applications**
   - Study algorithm complexity
   - Benchmark against other solvers
   - Develop new techniques

### Performance Optimization

#### Memory Management
```python
# For large batch processing
import gc

for scramble in many_scrambles:
    solution = solver.solve(cube)
    # Process solution
    gc.collect()  # Force garbage collection
```

#### Parallel Processing
```python
# For multiple independent solves
from concurrent.futures import ThreadPoolExecutor

def solve_single(scramble):
    cube = RubikCube()
    cube.execute_sequence(scramble)
    solver = AStarSolver()
    return solver.solve(cube)

with ThreadPoolExecutor(max_workers=4) as executor:
    solutions = list(executor.map(solve_single, scrambles))
```

---

## Troubleshooting

### Common Issues

#### Installation Problems

**Issue**: `ModuleNotFoundError: No module named 'numpy'`
**Solution**: 
```bash
pip install numpy matplotlib colorama pytest
```

**Issue**: `Permission denied` errors
**Solution**: 
```bash
# On Windows
pip install --user numpy matplotlib colorama pytest

# On Unix/Linux
sudo pip install numpy matplotlib colorama pytest
```

#### Runtime Errors

**Issue**: `ValueError: Invalid move notation`
**Solution**: Use standard notation (U, R', F2, etc.)
```python
# ❌ Wrong
cube.execute_move('up')

# ✅ Correct  
cube.execute_move('U')
```

**Issue**: `No solution found within time limits`
**Solutions:**
1. Increase timeout: `AStarSolver(timeout=120)`
2. Increase depth: `AStarSolver(max_depth=30)`
3. Use simpler heuristic: `heuristic_type='manhattan'`

**Issue**: `Memory errors with complex scrambles`
**Solutions:**
1. Reduce max_depth
2. Use timeout limits
3. Close other applications

#### Performance Issues

**Issue**: Very slow solving
**Diagnosis Steps:**
1. Check scramble complexity
2. Verify solver settings
3. Monitor system resources

**Solutions:**
1. Reduce max_depth for speed
2. Use faster heuristic
3. Set reasonable timeouts

**Issue**: Inconsistent results
**Causes:**
1. Random scrambles (use seeds for reproducibility)
2. Different solver settings
3. System resource variations

### Debug Mode

Enable debug output for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

cube = RubikCube()
solver = AStarSolver()
# Debug output will show search progress
```

### Getting Help

1. **Check Documentation**
   - API Reference for technical details
   - Algorithm Explanation for theory
   - This User Guide for practical usage

2. **Run Examples**
   - `examples/basic_usage.py`
   - `examples/performance_test.py`
   - `examples/demo_scrambles.py`

3. **Test Your Setup**
   ```bash
   python -m pytest src/tests/
   ```

4. **Common Solutions**
   - Restart Python interpreter
   - Check file permissions
   - Verify Python version (3.8+)
   - Update dependencies

---

## Next Steps

### Learning Path

1. **Master the Basics**
   - Understand cube notation
   - Practice with simple scrambles
   - Learn to interpret results

2. **Explore Advanced Features**
   - Try different heuristics
   - Experiment with settings
   - Use performance testing

3. **Apply Knowledge**
   - Solve real cube scrambles
   - Compare with other methods
   - Understand algorithm theory

4. **Contribute and Extend**
   - Modify algorithms
   - Add new features
   - Share improvements

### Additional Resources

- **Rubik's Cube Theory**: Study group theory and cube mathematics
- **Algorithm Design**: Learn about search algorithms and heuristics
- **Python Programming**: Improve Python skills for customization
- **Computer Science**: Explore AI and optimization techniques

### Community

This solver was developed for AeroHack 2025 - Collins Aerospace. It demonstrates practical applications of computer science concepts in aerospace engineering contexts, where algorithmic problem-solving and optimization are crucial skills.

---

*Happy solving! 🧩*