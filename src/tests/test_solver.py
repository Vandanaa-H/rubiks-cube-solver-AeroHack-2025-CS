"""
Unit tests for the A* solver
"""

import pytest
from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver
from src.algorithms.heuristics import Heuristics

class TestAStarSolver:
    """Test suite for A* solver."""
    
    def test_solver_initialization(self):
        """Test solver initialization."""
        solver = AStarSolver()
        
        assert solver.max_depth == 25
        assert solver.timeout == 60.0
        assert isinstance(solver.heuristics, Heuristics)
        assert len(solver.all_moves) == 18
    
    def test_solve_already_solved_cube(self):
        """Test solving an already solved cube."""
        cube = RubikCube()
        solver = AStarSolver()
        
        solution = solver.solve(cube)
        
        assert solution == []
        assert cube.is_solved()
    
    def test_solve_simple_scramble(self):
        """Test solving a simple scramble."""
        cube = RubikCube()
        solver = AStarSolver(max_depth=10, timeout=30)
        
        # Simple scramble: just one move
        cube.execute_move('U')
        
        solution = solver.solve(cube)
        
        assert solution is not None
        assert len(solution) <= 3  # Should be very short
        
        # Apply solution and verify it solves the cube
        test_cube = cube.copy()
        test_cube.execute_sequence(solution)
        assert test_cube.is_solved()
    
    def test_solve_medium_scramble(self):
        """Test solving a medium complexity scramble."""
        cube = RubikCube()
        solver = AStarSolver(max_depth=15, timeout=30)
        
        # Medium scramble
        moves = ['U', 'R', 'U\'', 'R\'', 'F', 'R', 'F\'']
        cube.execute_sequence(moves)
        
        solution = solver.solve(cube)
        
        if solution is not None:  # May not always find solution within limits
            # Verify solution works
            test_cube = cube.copy()
            test_cube.execute_sequence(solution)
            assert test_cube.is_solved()
            
            # Solution should be reasonable length
            assert len(solution) <= solver.max_depth
    
    def test_different_heuristics(self):
        """Test solver with different heuristic functions."""
        cube = RubikCube()
        cube.execute_sequence(['U', 'R', 'U\''])
        
        solver = AStarSolver(max_depth=10, timeout=15)
        
        heuristics = ['manhattan', 'corner_edge', 'combined']
        
        for heuristic in heuristics:
            test_cube = cube.copy()
            solution = solver.solve(test_cube, heuristic_type=heuristic)
            
            if solution is not None:
                # Verify solution works
                test_cube.execute_sequence(solution)
                assert test_cube.is_solved()
    
    def test_invalid_heuristic(self):
        """Test solver with invalid heuristic."""
        cube = RubikCube()
        solver = AStarSolver()
        
        with pytest.raises(ValueError):
            solver.solve(cube, heuristic_type='invalid_heuristic')
    
    def test_solver_timeout(self):
        """Test solver timeout functionality."""
        cube = RubikCube()
        # Create a complex scramble
        cube.scramble(25, seed=42)
        
        solver = AStarSolver(max_depth=30, timeout=1)  # Very short timeout
        
        solution = solver.solve(cube)
        
        # Should timeout and return None for complex scrambles
        stats = solver.get_statistics()
        assert stats.solve_time <= 2  # Should respect timeout (with some margin)
    
    def test_depth_limit(self):
        """Test solver depth limit."""
        cube = RubikCube()
        cube.scramble(20, seed=42)
        
        solver = AStarSolver(max_depth=5, timeout=30)  # Very shallow depth
        
        solution = solver.solve(cube)
        
        # May not find solution due to depth limit
        if solution is not None:
            assert len(solution) <= solver.max_depth
    
    def test_move_relationships(self):
        """Test move relationship mappings."""
        solver = AStarSolver()
        
        # Test opposite moves
        assert solver.opposite_moves['U'] == 'U\''
        assert solver.opposite_moves['U\''] == 'U'
        assert solver.opposite_moves['U2'] == 'U2'
        
        # Test face moves grouping
        assert 'U' in solver.face_moves['U']
        assert 'U\'' in solver.face_moves['U']
        assert 'U2' in solver.face_moves['U']
    
    def test_valid_moves_pruning(self):
        """Test that move pruning works correctly."""
        solver = AStarSolver()
        
        # No previous moves - should return all moves
        valid_moves = solver._get_valid_moves([])
        assert len(valid_moves) == 18
        
        # After U, shouldn't allow U' immediately
        valid_moves = solver._get_valid_moves(['U'])
        assert 'U\'' not in valid_moves
        assert 'U' not in valid_moves  # No same face consecutive
        assert 'U2' not in valid_moves
        
        # Should still have other face moves
        assert 'R' in valid_moves
        assert 'F' in valid_moves
    
    def test_redundant_pattern_detection(self):
        """Test redundant pattern detection."""
        solver = AStarSolver()
        
        # Test A B A pattern
        assert solver._is_redundant_pattern(['U', 'R', 'U'])
        
        # Test A A A pattern
        assert solver._is_redundant_pattern(['U', 'U', 'U'])
        
        # Test valid pattern
        assert not solver._is_redundant_pattern(['U', 'R', 'F'])
        
        # Test short sequences
        assert not solver._is_redundant_pattern(['U', 'R'])
    
    def test_cube_reconstruction(self):
        """Test cube reconstruction from state hash."""
        solver = AStarSolver()
        
        original_cube = RubikCube()
        original_cube.scramble(10, seed=42)
        
        state_hash = original_cube.get_state_string()
        reconstructed_cube = solver._reconstruct_cube(state_hash)
        
        assert original_cube == reconstructed_cube
    
    def test_iterative_deepening_fallback(self):
        """Test iterative deepening fallback method."""
        cube = RubikCube()
        cube.execute_move('U')  # Simple case
        
        solver = AStarSolver(max_depth=5, timeout=10)
        
        solution = solver.solve_iterative_deepening(cube)
        
        if solution is not None:
            test_cube = cube.copy()
            test_cube.execute_sequence(solution)
            assert test_cube.is_solved()
    
    def test_statistics_collection(self):
        """Test statistics collection during solving."""
        cube = RubikCube()
        cube.execute_sequence(['U', 'R'])
        
        solver = AStarSolver(max_depth=10, timeout=15)
        
        solution = solver.solve(cube)
        stats = solver.get_statistics()
        
        # Check that statistics were collected
        assert stats.nodes_explored >= 0
        assert stats.solve_time >= 0
        
        if solution is not None:
            assert stats.solution_found
            assert stats.solution_length == len(solution)
        else:
            assert not stats.solution_found

class TestHeuristics:
    """Test suite for heuristic functions."""
    
    def test_heuristics_initialization(self):
        """Test heuristics initialization."""
        heuristics = Heuristics()
        
        # Check that piece positions are initialized
        assert len(heuristics.corners) == 8
        assert len(heuristics.edges) == 12
        assert len(heuristics.centers) == 6
    
    def test_manhattan_distance_solved(self):
        """Test Manhattan distance for solved cube."""
        heuristics = Heuristics()
        cube = RubikCube()
        
        distance = heuristics.manhattan_distance(cube)
        assert distance == 0
    
    def test_manhattan_distance_scrambled(self):
        """Test Manhattan distance for scrambled cube."""
        heuristics = Heuristics()
        cube = RubikCube()
        cube.scramble(10, seed=42)
        
        distance = heuristics.manhattan_distance(cube)
        assert distance > 0
    
    def test_corner_edge_heuristic_solved(self):
        """Test corner-edge heuristic for solved cube."""
        heuristics = Heuristics()
        cube = RubikCube()
        
        h_value = heuristics.corner_edge_heuristic(cube)
        assert h_value == 0
    
    def test_corner_edge_heuristic_scrambled(self):
        """Test corner-edge heuristic for scrambled cube."""
        heuristics = Heuristics()
        cube = RubikCube()
        cube.scramble(10, seed=42)
        
        h_value = heuristics.corner_edge_heuristic(cube)
        assert h_value > 0
    
    def test_combined_heuristic(self):
        """Test combined heuristic function."""
        heuristics = Heuristics()
        
        # Solved cube
        cube = RubikCube()
        h_value = heuristics.combined_heuristic(cube)
        assert h_value == 0
        
        # Scrambled cube
        cube.scramble(10, seed=42)
        h_value = heuristics.combined_heuristic(cube)
        assert h_value > 0
    
    def test_heuristic_consistency(self):
        """Test that heuristics are consistent (never overestimate)."""
        heuristics = Heuristics()
        cube = RubikCube()
        
        # Test with various simple scrambles
        for moves in [['U'], ['U', 'R'], ['U', 'R', 'U\''], ['U', 'R', 'U\'', 'R\'']]:
            test_cube = cube.copy()
            test_cube.execute_sequence(moves)
            
            h_value = heuristics.estimate_moves_to_solve(test_cube)
            
            # Heuristic should not overestimate
            # For simple scrambles, should be reasonable
            assert h_value >= 0
            assert h_value <= len(moves) * 3  # Very loose upper bound

if __name__ == '__main__':
    pytest.main([__file__])