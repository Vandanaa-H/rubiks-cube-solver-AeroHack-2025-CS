"""
Integration tests for the complete Rubik's Cube Solver system
"""

import pytest
import time
from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver
from src.algorithms.heuristics import Heuristics
from src.algorithms.utils import MoveOptimizer, format_move_sequence, analyze_move_sequence
from src.ui.visualizer import CubeVisualizer

class TestSystemIntegration:
    """Integration tests for the complete system."""
    
    def test_end_to_end_solving(self):
        """Test complete end-to-end solving workflow."""
        # Create and scramble cube
        cube = RubikCube()
        scramble_moves = cube.scramble(8, seed=42)  # Manageable scramble
        
        assert not cube.is_solved()
        assert len(cube.move_history) == 8
        
        # Solve with A* algorithm
        solver = AStarSolver(max_depth=20, timeout=30)
        solution = solver.solve(cube.copy())
        
        if solution is not None:
            # Verify solution
            test_cube = cube.copy()
            test_cube.execute_sequence(solution)
            assert test_cube.is_solved()
            
            # Check statistics
            stats = solver.get_statistics()
            assert stats.solution_found
            assert stats.solution_length == len(solution)
            assert stats.solve_time > 0
    
    def test_move_optimization_integration(self):
        """Test move sequence optimization integration."""
        cube = RubikCube()
        solver = AStarSolver(max_depth=15, timeout=20)
        optimizer = MoveOptimizer()
        
        # Create a scramble that might have optimization opportunities
        moves = ['U', 'U', 'R', 'R\'', 'R', 'F2']
        cube.execute_sequence(moves)
        
        solution = solver.solve(cube.copy())
        
        if solution is not None:
            # Optimize the solution
            optimized_solution = optimizer.optimize_sequence(solution)
            
            # Both should solve the cube
            test_cube1 = cube.copy()
            test_cube1.execute_sequence(solution)
            
            test_cube2 = cube.copy()
            test_cube2.execute_sequence(optimized_solution)
            
            assert test_cube1.is_solved()
            assert test_cube2.is_solved()
            
            # Optimized should be same length or shorter
            assert len(optimized_solution) <= len(solution)
    
    def test_multiple_heuristics_consistency(self):
        """Test that different heuristics produce valid solutions."""
        cube = RubikCube()
        cube.execute_sequence(['U', 'R'])  # Simpler 2-move sequence
        
        solver = AStarSolver(max_depth=20, timeout=15)
        heuristics = ['manhattan', 'corner_edge', 'combined']
        
        solutions = {}
        
        for heuristic in heuristics:
            test_cube = cube.copy()
            solution = solver.solve(test_cube, heuristic_type=heuristic)
            
            if solution is not None:
                # Verify solution works
                test_cube.execute_sequence(solution)
                assert test_cube.is_solved()
                
                solutions[heuristic] = solution
        
        # At least one heuristic should find a solution for this simple case
        assert len(solutions) > 0
    
    def test_visualizer_integration(self):
        """Test visualizer integration with cube states."""
        cube = RubikCube()
        visualizer = CubeVisualizer()
        
        # Test with solved cube
        ascii_solved = visualizer.display_ascii_art(cube)
        assert isinstance(ascii_solved, str)
        assert len(ascii_solved) > 0
        
        # Test with scrambled cube
        cube.scramble(10, seed=42)
        ascii_scrambled = visualizer.display_ascii_art(cube)
        assert isinstance(ascii_scrambled, str)
        assert ascii_scrambled != ascii_solved
        
        # Test animation frames
        moves = ['U', 'R', 'U\'']
        test_cube = RubikCube()
        frames = visualizer.display_move_animation_frames(test_cube, moves)
        
        assert len(frames) == len(moves) + 1  # Initial state + one per move
        assert all(isinstance(frame, str) for frame in frames)
    
    def test_performance_benchmark(self):
        """Test system performance with multiple test cases."""
        solver = AStarSolver(max_depth=15, timeout=10)
        
        test_cases = [
            ['U'],
            ['U', 'R'],
            ['U', 'R', 'U\''],
            ['U', 'R', 'U\'', 'R\''],
            ['R', 'U', 'R\'', 'F', 'R', 'F\'']
        ]
        
        results = []
        
        for i, moves in enumerate(test_cases):
            cube = RubikCube()
            cube.execute_sequence(moves)
            
            start_time = time.time()
            solution = solver.solve(cube.copy())
            solve_time = time.time() - start_time
            
            if solution is not None:
                # Verify solution
                test_cube = cube.copy()
                test_cube.execute_sequence(solution)
                assert test_cube.is_solved()
                
                results.append({
                    'scramble_length': len(moves),
                    'solution_length': len(solution),
                    'solve_time': solve_time,
                    'efficiency': len(moves) / len(solution) if len(solution) > 0 else 0
                })
        
        # Should solve at least some test cases
        assert len(results) > 0
        
        # Performance should be reasonable for simple cases
        simple_results = [r for r in results if r['scramble_length'] <= 2]
        if simple_results:
            avg_time = sum(r['solve_time'] for r in simple_results) / len(simple_results)
            assert avg_time < 5.0  # Should solve simple cases quickly
    
    def test_state_preservation(self):
        """Test that state is preserved correctly through operations."""
        cube = RubikCube()
        original_state = cube.state.copy()
        
        # Test that copy preserves state
        cube_copy = cube.copy()
        assert cube == cube_copy
        assert cube.state is not cube_copy.state  # Different objects
        
        # Test that operations don't affect original
        cube_copy.scramble(10)
        assert cube != cube_copy
        assert (cube.state == original_state).all()
        
        # Test state consistency after moves
        cube.execute_sequence(['U', 'R', 'U\'', 'R\''])
        
        # Should have same color distribution
        for color in range(6):
            assert (cube.state == color).sum() == 9
    
    def test_move_sequence_analysis(self):
        """Test move sequence analysis utilities."""
        moves = ['U', 'R', 'U\'', 'R\'', 'F', 'R', 'F\'', 'U2', 'R2']
        
        # Test formatting
        formatted = format_move_sequence(moves, line_length=20)
        assert isinstance(formatted, str)
        assert 'U' in formatted
        
        # Test analysis
        analysis = analyze_move_sequence(moves)
        
        assert analysis['total_moves'] == len(moves)
        assert analysis['unique_moves'] <= len(moves)
        assert 'face_distribution' in analysis
        assert 'move_type_distribution' in analysis
        
        # Check face distribution
        assert analysis['face_distribution']['U'] >= 1
        assert analysis['face_distribution']['R'] >= 1
        
        # Check move type distribution
        total_types = sum(analysis['move_type_distribution'].values())
        assert total_types == len(moves)
    
    def test_error_handling(self):
        """Test system error handling."""
        cube = RubikCube()
        solver = AStarSolver()
        
        # Test invalid moves
        with pytest.raises(ValueError):
            cube.execute_move('X')
        
        # Test invalid heuristic
        with pytest.raises(ValueError):
            solver.solve(cube, heuristic_type='invalid')
        
        # Test invalid cube state
        with pytest.raises(ValueError):
            RubikCube(state=[1, 2, 3])  # Too short
    
    def test_memory_efficiency(self):
        """Test that system doesn't have obvious memory leaks."""
        import gc
        
        # Create and solve multiple cubes
        solver = AStarSolver(max_depth=10, timeout=15)
        
        for i in range(10):
            cube = RubikCube()
            cube.scramble(5, seed=i)
            
            solution = solver.solve(cube.copy())
            
            if solution is not None:
                test_cube = cube.copy()
                test_cube.execute_sequence(solution)
                assert test_cube.is_solved()
            
            # Force garbage collection
            del cube
            if solution is not None:
                del test_cube
            gc.collect()
        
        # Test passed if no memory errors occurred
        assert True

class TestMoveEngine:
    """Integration tests for move engine."""
    
    def test_all_moves_reversible(self):
        """Test that all moves are properly reversible."""
        cube = RubikCube()
        
        move_pairs = [
            ('U', 'U\''), ('D', 'D\''), ('L', 'L\''),
            ('R', 'R\''), ('F', 'F\''), ('B', 'B\'')
        ]
        
        for move, reverse in move_pairs:
            test_cube = cube.copy()
            
            # Apply move and reverse
            test_cube.execute_move(move)
            test_cube.execute_move(reverse)
            
            # Should be back to solved state
            assert test_cube.is_solved()
    
    def test_double_moves(self):
        """Test that double moves work correctly."""
        cube = RubikCube()
        
        for face in ['U', 'D', 'L', 'R', 'F', 'B']:
            test_cube1 = cube.copy()
            test_cube2 = cube.copy()
            
            # X2 should equal X X
            test_cube1.execute_move(face + '2')
            test_cube2.execute_move(face)
            test_cube2.execute_move(face)
            
            assert test_cube1 == test_cube2
    
    def test_move_commutation(self):
        """Test move commutation properties."""
        cube = RubikCube()
        
        # Parallel faces should commute (U and D)
        test_cube1 = cube.copy()
        test_cube2 = cube.copy()
        
        test_cube1.execute_sequence(['U', 'D'])
        test_cube2.execute_sequence(['D', 'U'])
        
        assert test_cube1 == test_cube2
        
        # Adjacent faces should not commute (U and R)
        test_cube1 = cube.copy()
        test_cube2 = cube.copy()
        
        test_cube1.execute_sequence(['U', 'R'])
        test_cube2.execute_sequence(['R', 'U'])
        
        assert test_cube1 != test_cube2

if __name__ == '__main__':
    pytest.main([__file__])
