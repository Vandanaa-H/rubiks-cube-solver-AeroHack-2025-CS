#!/usr/bin/env python3
"""
Performance test and benchmark for the Rubik's Cube Solver.
Measures solving speed and efficiency across different scenarios.
"""

import sys
import os
import time
import statistics

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver

def benchmark_solver(scramble_length: int, num_tests: int = 5, timeout: int = 10) -> dict:
    """Benchmark solver performance for given scramble length."""
    print(f"\n Benchmarking {scramble_length}-move scrambles ({num_tests} tests)...")
    
    solver = AStarSolver(max_depth=20, timeout=timeout)
    results = {
        'scramble_length': scramble_length,
        'solve_times': [],
        'solution_lengths': [],
        'success_rate': 0,
        'average_time': 0,
        'average_solution_length': 0
    }
    
    successes = 0
    
    for test_num in range(num_tests):
        cube = RubikCube()
        scramble_moves = cube.scramble(scramble_length, seed=42 + test_num)
        
        print(f"   Test {test_num + 1}: {' '.join(scramble_moves)}")
        
        start_time = time.time()
        solution = solver.solve(cube.copy())
        solve_time = time.time() - start_time
        
        if solution:
            successes += 1
            results['solve_times'].append(solve_time)
            results['solution_lengths'].append(len(solution))
            print(f"      Solved in {solve_time:.3f}s with {len(solution)} moves")
        else:
            print(f"      Failed to solve in {timeout}s")
    
    # Calculate statistics
    results['success_rate'] = (successes / num_tests) * 100
    
    if results['solve_times']:
        results['average_time'] = statistics.mean(results['solve_times'])
        results['average_solution_length'] = statistics.mean(results['solution_lengths'])
    
    return results

def test_heuristic_performance():
    """Test performance of different heuristics."""
    print("\n Testing heuristic performance...")
    
    heuristics = ['manhattan', 'corner_edge', 'combined']
    cube = RubikCube()
    cube.execute_sequence(['U', 'R', 'U\'', 'R\''])  # Simple test case
    
    for heuristic in heuristics:
        print(f"\n   Testing {heuristic} heuristic:")
        solver = AStarSolver(max_depth=15, timeout=5)
        
        start_time = time.time()
        solution = solver.solve(cube.copy(), heuristic_type=heuristic)
        solve_time = time.time() - start_time
        
        if solution:
            print(f"        Solved in {solve_time:.3f}s with {len(solution)} moves")
        else:
            print(f"      Failed to solve in 5s")

def main():
    """Run comprehensive performance tests."""
    print("Rubik's Cube Solver - Performance Test Suite")
    print("=" * 55)
    
    # Test basic functionality first
    print("\n1. Basic functionality test...")
    cube = RubikCube()
    assert cube.is_solved(), "Cube should start solved"
    cube.execute_move('U')
    assert not cube.is_solved(), "Cube should not be solved after move"
    print("  Basic functionality OK")
    
    # Benchmark different scramble lengths
    benchmark_results = []
    
    for scramble_length in [3, 5, 8]:
        result = benchmark_solver(scramble_length, num_tests=3, timeout=15)
        benchmark_results.append(result)
    
    # Test heuristic performance
    test_heuristic_performance()
    
    # Print summary
    print("\n" + "=" * 55)
    print(" PERFORMANCE SUMMARY")
    print("=" * 55)
    
    for result in benchmark_results:
        length = result['scramble_length']
        success = result['success_rate']
        avg_time = result['average_time']
        avg_moves = result['average_solution_length']
        
        print(f"  {length}-move scrambles:")
        print(f"    Success rate: {success:.1f}%")
        if avg_time > 0:
            print(f"    Average time: {avg_time:.3f}s")
            print(f"    Average solution: {avg_moves:.1f} moves")
        print()
    
    # Performance recommendations
    print(" Performance Notes:")
    print("   - 3-5 move scrambles: Should solve quickly (<1s)")
    print("   - 8+ move scrambles: May require longer search times")
    print("   - corner_edge heuristic typically provides best balance")
    print("   - Increase max_depth for harder scrambles")

if __name__ == "__main__":
    main()
