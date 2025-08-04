"""
Rubik's Cube Solver - Main Entry Point
AeroHack 2025 - Collins Aerospace
Author: Vandana
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.console_interface import ConsoleInterface
from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver

def main():
    """Main entry point for the Rubik's Cube Solver."""
    print(" RUBIK'S CUBE SOLVER")
    print("AeroHack 2025 - Collins Aerospace")
    print("Algorithmic Puzzle Solving Challenge")
    print("=" * 50)
    
    # Initialize components
    cube = RubikCube()
    solver = AStarSolver()
    interface = ConsoleInterface(cube, solver)
    
    # Start the interactive interface
    interface.run()

if __name__ == "__main__":
    main()