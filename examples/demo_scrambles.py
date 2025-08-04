"""
Demo scrambles and showcase examples for the Rubik's Cube Solver
Includes famous algorithms and interesting cube states.
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver
from src.ui.visualizer import CubeVisualizer
from src.algorithms.utils import format_move_sequence, analyze_move_sequence

class DemoScrambles:
    """Collection of demo scrambles and interesting cube states."""
    
    def __init__(self):
        """Initialize demo scrambles collection."""
        self.solver = AStarSolver(max_depth=20, timeout=45)
        self.visualizer = CubeVisualizer()
        
        # Famous algorithms and patterns
        self.algorithms = {
            "Sexy Move": ['R', 'U', 'R\'', 'U\''],
            "T-Perm": ['R', 'U', 'R\'', 'F\'', 'R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R2', 'U\'', 'R\''],
            "Sune": ['R', 'U', 'R\'', 'U', 'R', 'U2', 'R\''],
            "Anti-Sune": ['R', 'U2', 'R\'', 'U\'', 'R', 'U\'', 'R\''],
            "J-Perm": ['R', 'U', 'R\'', 'F\'', 'R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R2', 'U\'', 'R\''],
            "Y-Perm": ['F', 'R', 'U\'', 'R\'', 'U\'', 'R', 'U', 'R\'', 'F\'', 'R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R', 'F\''],
            "Superflip": ['U', 'R2', 'F', 'B', 'R', 'B2', 'R', 'U2', 'L', 'B2', 'R', 'U\'', 'D\'', 'R2', 'F', 'R\'', 'L', 'B2', 'U2', 'F2']
        }
        
        # Easy teaching scrambles
        self.easy_scrambles = {
            "Single Move": ['U'],
            "Two Moves": ['U', 'R'],
            "Beginner": ['U', 'R', 'U\'', 'R\''],
            "Layer": ['U', 'R', 'U\'', 'R\'', 'F', 'R', 'F\''],
            "Cross": ['F', 'R', 'U\'', 'R\'', 'F\'', 'U'],
            "Corner": ['R', 'U', 'R\'', 'U', 'R', 'U2', 'R\'', 'U']
        }
        
        # Medium complexity scrambles
        self.medium_scrambles = {
            "Standard 1": ['U', 'R2', 'F', 'B', 'R', 'B2', 'R', 'U2', 'L', 'B2'],
            "Standard 2": ['R', 'U', 'R\'', 'D', 'R', 'U\'', 'R\'', 'D\'', 'R2', 'U'],
            "Mixed Faces": ['F', 'D', 'L\'', 'B', 'U\'', 'R', 'F\'', 'U', 'L', 'D\''],
            "Rotation Heavy": ['R2', 'U2', 'R2', 'D2', 'L2', 'F2', 'B2', 'U2'],
            "Complex": ['R', 'U\'', 'R', 'F\'', 'R2', 'U\'', 'R\'', 'U\'', 'R', 'U', 'R\'', 'F']
        }
        
        # Hard scrambles (may timeout)
        self.hard_scrambles = {
            "Challenge 1": ['R', 'U2', 'R\'', 'D\'', 'R', 'U\'', 'R\'', 'D', 'R\'', 'U\'', 'R', 'U\'', 'R\'', 'U', 'R', 'U'],
            "Challenge 2": ['F', 'R', 'U\'', 'R\'', 'U\'', 'R', 'U', 'R\'', 'F\'', 'R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R2', 'U\''],
            "Advanced": ['R2', 'D2', 'R', 'U2', 'R', 'D2', 'R\'', 'U2', 'R\'', 'B2', 'D', 'B2', 'U\'', 'B2', 'D\'', 'B2'],
            "Expert": ['U', 'R2', 'F', 'B', 'R', 'B2', 'R', 'U2', 'L', 'B2', 'R', 'U\'', 'D\'', 'R2', 'F', 'R\'', 'L', 'B2', 'U2'],
            "Master": ['R', 'U', 'R\'', 'F\'', 'R', 'U2', 'R\'', 'U2', 'R\'', 'F', 'R', 'F\'', 'U\'', 'F', 'R', 'U', 'R\'', 'F\'', 'R2']
        }

    def demo_algorithm(self, name: str, moves: list, solve: bool = True) -> None:
        """
        Demonstrate a specific algorithm.
        
        Args:
            name: Algorithm name
            moves: List of moves
            solve: Whether to solve after demo
        """
        print(f"\n DEMONSTRATING: {name}")
        print("=" * 50)
        
        cube = RubikCube()
        print("Starting with solved cube...")
        
        # Show algorithm
        print(f"\nAlgorithm: {' '.join(moves)}")
        print(f"Length: {len(moves)} moves")
        
        # Analyze the algorithm
        analysis = analyze_move_sequence(moves)
        print(f"\nAlgorithm Analysis:")
        for key, value in analysis.items():
            if key != 'face_distribution':
                print(f"  {key}: {value}")
        
        # Execute algorithm
        print(f"\n Executing algorithm...")
        cube.execute_sequence(moves)
        
        print(f"Cube solved after algorithm: {cube.is_solved()}")
        
        # Show ASCII representation
        print(f"\nCube state after algorithm:")
        ascii_art = self.visualizer.display_ascii_art(cube)
        print(ascii_art)
        
        # Solve if requested
        if solve and not cube.is_solved():
            print(f"\n Solving cube...")
            start_time = time.time()
            solution = self.solver.solve(cube.copy())
            solve_time = time.time() - start_time
            
            if solution:
                print(f" Solution found!")
                print(f"Solution length: {len(solution)} moves")
                print(f"Solve time: {solve_time:.2f}s")
                print(f"Solution: {format_move_sequence(solution, 40)}")
                
                # Verify solution
                test_cube = cube.copy()
                test_cube.execute_sequence(solution)
                print(f"Verification: {test_cube.is_solved()}")
                
            else:
                print(f" Could not solve within time limits")
                print(f"Time spent: {solve_time:.2f}s")

    def demo_scramble_category(self, category_name: str, scrambles: dict) -> None:
        """
        Demo a category of scrambles.
        
        Args:
            category_name: Name of the category
            scrambles: Dictionary of scramble name -> moves
        """
        print(f"\n {category_name.upper()} SCRAMBLES DEMO")
        print("=" * 60)
        
        results = []
        
        for name, moves in scrambles.items():
            print(f"\n Testing: {name}")
            print(f"Scramble: {' '.join(moves)} ({len(moves)} moves)")
            
            # Create and scramble cube
            cube = RubikCube()
            cube.execute_sequence(moves)
            
            # Solve
            start_time = time.time()
            solution = self.solver.solve(cube.copy())
            solve_time = time.time() - start_time
            
            if solution:
                efficiency = len(moves) / len(solution) if len(solution) > 0 else 0
                print(f" Solved: {len(solution)} moves, {solve_time:.2f}s (efficiency: {efficiency:.2f})")
                
                results.append({
                    'name': name,
                    'scramble_length': len(moves),
                    'solution_length': len(solution),
                    'solve_time': solve_time,
                    'efficiency': efficiency,
                    'success': True
                })
                
            else:
                print(f" Failed: {solve_time:.2f}s timeout")
                results.append({
                    'name': name,
                    'scramble_length': len(moves),
                    'solve_time': solve_time,
                    'success': False
                })
        
        # Summary
        successful = [r for r in results if r['success']]
        print(f"\n {category_name} Summary:")
        print(f"Success rate: {len(successful)}/{len(results)} ({100*len(successful)/len(results):.1f}%)")
        
        if successful:
            avg_solve_time = sum(r['solve_time'] for r in successful) / len(successful)
            avg_solution_length = sum(r['solution_length'] for r in successful) / len(successful)
            avg_efficiency = sum(r['efficiency'] for r in successful) / len(successful)
            
            print(f"Average solve time: {avg_solve_time:.2f}s")
            print(f"Average solution length: {avg_solution_length:.1f} moves")
            print(f"Average efficiency: {avg_efficiency:.2f}")

    def interactive_demo(self) -> None:
        """Interactive demo allowing user to choose scrambles."""
        print(f"\n INTERACTIVE DEMO MODE")
        print("=" * 40)
        
        categories = {
            '1': ('Famous Algorithms', self.algorithms),
            '2': ('Easy Scrambles', self.easy_scrambles),
            '3': ('Medium Scrambles', self.medium_scrambles),
            '4': ('Hard Scrambles', self.hard_scrambles)
        }
        
        while True:
            print(f"\nSelect a category:")
            for key, (name, _) in categories.items():
                print(f"{key}. {name}")
            print("0. Exit")
            
            choice = input(f"\nEnter choice (0-4): ").strip()
            
            if choice == '0':
                break
            elif choice in categories:
                category_name, scrambles = categories[choice]
                
                print(f"\n{category_name} options:")
                scramble_list = list(scrambles.items())
                for i, (name, moves) in enumerate(scramble_list, 1):
                    print(f"{i}. {name} ({len(moves)} moves)")
                print("0. Back to categories")
                
                while True:
                    subchoice = input(f"\nSelect scramble (0-{len(scramble_list)}): ").strip()
                    
                    if subchoice == '0':
                        break
                    elif subchoice.isdigit() and 1 <= int(subchoice) <= len(scramble_list):
                        idx = int(subchoice) - 1
                        name, moves = scramble_list[idx]
                        
                        if choice == '1':  # Algorithms
                            self.demo_algorithm(name, moves)
                        else:  # Scrambles
                            print(f"\n TESTING: {name}")
                            print("=" * 40)
                            
                            cube = RubikCube()
                            cube.execute_sequence(moves)
                            
                            print(f"Scramble: {' '.join(moves)}")
                            print(f"Solving...")
                            
                            solution = self.solver.solve(cube.copy())
                            if solution:
                                print(f" Solution: {len(solution)} moves")
                                print(f"Moves: {format_move_sequence(solution, 50)}")
                            else:
                                print(f" Could not solve within limits")
                        
                        input(f"\nPress Enter to continue...")
                        break
                    else:
                        print("Invalid choice. Try again.")
            else:
                print("Invalid choice. Try again.")

    def benchmark_suite(self) -> None:
        """Run complete benchmark suite."""
        print(f"\n COMPLETE BENCHMARK SUITE")
        print("=" * 50)
        
        # Test all categories
        self.demo_scramble_category("Easy", self.easy_scrambles)
        self.demo_scramble_category("Medium", self.medium_scrambles)
        self.demo_scramble_category("Hard", self.hard_scrambles)
        
        print(f"\n BENCHMARK COMPLETE")
        print("All scramble categories have been tested!")

    def showcase_algorithms(self) -> None:
        """Showcase famous Rubik's cube algorithms."""
        print(f"\n FAMOUS ALGORITHMS SHOWCASE")
        print("=" * 50)
        
        showcase_algorithms = ['Sexy Move', 'Sune', 'T-Perm']
        
        for alg_name in showcase_algorithms:
            if alg_name in self.algorithms:
                self.demo_algorithm(alg_name, self.algorithms[alg_name], solve=True)
                input(f"\nPress Enter to continue to next algorithm...")

    def visualization_showcase(self) -> None:
        """Showcase visualization capabilities."""
        print(f"\n VISUALIZATION SHOWCASE")
        print("=" * 40)
        
        cube = RubikCube()
        
        print("1. Solved cube:")
        ascii_art = self.visualizer.display_ascii_art(cube)
        print(ascii_art)
        
        print(f"\n2. After Sexy Move algorithm:")
        cube.execute_sequence(self.algorithms['Sexy Move'])
        ascii_art = self.visualizer.display_ascii_art(cube)
        print(ascii_art)
        
        print(f"\n3. After additional scrambling:")
        cube.scramble(8, seed=123)
        ascii_art = self.visualizer.display_ascii_art(cube)
        print(ascii_art)
        
        print(f"\n4. Detailed console view:")
        self.visualizer.display_detailed_console(cube)

def main():
    """Main demo function."""
    print(" RUBIK'S CUBE SOLVER - DEMO SCRAMBLES")
    print("AeroHack 2025 - Collins Aerospace")
    print("=" * 60)
    
    demo = DemoScrambles()
    
    print(f"\nDemo Options:")
    print(f"1. Interactive Demo")
    print(f"2. Algorithm Showcase")
    print(f"3. Benchmark Suite")
    print(f"4. Visualization Showcase")
    print(f"5. Run All Demos")
    
    try:
        choice = input(f"\nSelect demo (1-5): ").strip()
        
        if choice == '1':
            demo.interactive_demo()
        elif choice == '2':
            demo.showcase_algorithms()
        elif choice == '3':
            demo.benchmark_suite()
        elif choice == '4':
            demo.visualization_showcase()
        elif choice == '5':
            print(f"\n Running all demos...")
            demo.showcase_algorithms()
            demo.visualization_showcase()
            demo.benchmark_suite()
        else:
            print(f"Invalid choice. Running interactive demo...")
            demo.interactive_demo()
        
        print(f"\n Demo completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n\n Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n Error in demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()