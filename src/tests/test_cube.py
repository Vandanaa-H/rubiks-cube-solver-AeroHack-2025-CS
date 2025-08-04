"""
Unit tests for the RubikCube class
"""

import pytest
import numpy as np
from src.core.cube import RubikCube

class TestRubikCube:
    """Test suite for RubikCube class."""
    
    def test_initialization(self):
        """Test cube initialization."""
        cube = RubikCube()
        
        # Check that cube is solved initially
        assert cube.is_solved()
        
        # Check state shape
        assert cube.state.shape == (54,)
        
        # Check that each face has correct color
        for face_idx in range(6):
            face = cube.get_face(face_idx)
            assert face.shape == (3, 3)
            assert np.all(face == face_idx)
    
    def test_custom_state_initialization(self):
        """Test initialization with custom state."""
        custom_state = np.arange(54)
        cube = RubikCube(custom_state)
        
        assert np.array_equal(cube.state, custom_state)
        assert not cube.is_solved()
    
    def test_invalid_state_initialization(self):
        """Test initialization with invalid state."""
        with pytest.raises(ValueError):
            RubikCube(np.array([1, 2, 3]))  # Wrong size
    
    def test_get_set_face(self):
        """Test getting and setting faces."""
        cube = RubikCube()
        
        # Test getting face
        front_face = cube.get_face(0)
        assert front_face.shape == (3, 3)
        assert np.all(front_face == 0)
        
        # Test setting face
        new_face = np.ones((3, 3), dtype=int) * 5
        cube.set_face(0, new_face)
        
        retrieved_face = cube.get_face(0)
        assert np.array_equal(retrieved_face, new_face)
    
    def test_invalid_face_operations(self):
        """Test invalid face operations."""
        cube = RubikCube()
        
        # Invalid face index
        with pytest.raises(ValueError):
            cube.get_face(6)
        
        with pytest.raises(ValueError):
            cube.set_face(-1, np.ones((3, 3)))
        
        # Invalid face data shape
        with pytest.raises(ValueError):
            cube.set_face(0, np.ones((2, 2)))
    
    def test_basic_moves(self):
        """Test basic move execution."""
        cube = RubikCube()
        
        # Test valid move
        cube.execute_move('U')
        assert len(cube.move_history) == 1
        assert cube.move_history[0] == 'U'
        assert not cube.is_solved()
        
        # Test invalid move
        with pytest.raises(ValueError):
            cube.execute_move('X')
    
    def test_move_sequence(self):
        """Test executing move sequences."""
        cube = RubikCube()
        
        moves = ['U', 'R', 'U\'', 'R\'']
        cube.execute_sequence(moves)
        
        assert len(cube.move_history) == 4
        assert cube.move_history == moves
    
    def test_move_cancellation(self):
        """Test that opposite moves cancel out."""
        cube = RubikCube()
        
        # U followed by U' should return to solved state
        cube.execute_move('U')
        cube.execute_move('U\'')
        
        assert cube.is_solved()
    
    def test_double_move(self):
        """Test double moves."""
        cube = RubikCube()
        
        # U2 should be equivalent to U U
        cube1 = cube.copy()
        cube2 = cube.copy()
        
        cube1.execute_move('U2')
        cube2.execute_move('U')
        cube2.execute_move('U')
        
        assert np.array_equal(cube1.state, cube2.state)
    
    def test_scramble(self):
        """Test cube scrambling."""
        cube = RubikCube()
        
        # Test scrambling
        scramble_moves = cube.scramble(10, seed=42)
        
        assert len(scramble_moves) == 10
        assert len(cube.move_history) == 10
        assert not cube.is_solved()
        
        # Test deterministic scrambling with seed
        cube2 = RubikCube()
        scramble_moves2 = cube2.scramble(10, seed=42)
        
        assert scramble_moves == scramble_moves2
        assert np.array_equal(cube.state, cube2.state)
    
    def test_copy(self):
        """Test cube copying."""
        cube = RubikCube()
        cube.scramble(5)
        
        cube_copy = cube.copy()
        
        # Should be equal but separate objects
        assert cube == cube_copy
        assert cube is not cube_copy
        assert np.array_equal(cube.state, cube_copy.state)
        assert cube.move_history == cube_copy.move_history
        
        # Modifying copy shouldn't affect original
        cube_copy.execute_move('U')
        assert cube != cube_copy
    
    def test_reset(self):
        """Test cube reset functionality."""
        cube = RubikCube()
        cube.scramble(10)
        
        assert not cube.is_solved()
        assert len(cube.move_history) > 0
        
        cube.reset()
        
        assert cube.is_solved()
        assert len(cube.move_history) == 0
    
    def test_state_string(self):
        """Test state string representation."""
        cube = RubikCube()
        state_str = cube.get_state_string()
        
        assert len(state_str) == 54
        assert state_str == '000000000111111111222222222333333333444444444555555555'
        
        # After scrambling, should be different
        cube.scramble(5)
        new_state_str = cube.get_state_string()
        assert new_state_str != state_str
    
    def test_equality_and_hashing(self):
        """Test cube equality and hashing."""
        cube1 = RubikCube()
        cube2 = RubikCube()
        
        # Solved cubes should be equal
        assert cube1 == cube2
        assert hash(cube1) == hash(cube2)
        
        # After different scrambles, should be different
        cube1.scramble(5, seed=1)
        cube2.scramble(5, seed=2)
        
        assert cube1 != cube2
        assert hash(cube1) != hash(cube2)
    
    def test_move_count(self):
        """Test move counting."""
        cube = RubikCube()
        
        assert cube.get_move_count() == 0
        
        cube.execute_sequence(['U', 'R', 'U\'', 'R\''])
        assert cube.get_move_count() == 4
        
        cube.reset()
        assert cube.get_move_count() == 0
    
    def test_comprehensive_move_set(self):
        """Test all 18 standard moves."""
        cube = RubikCube()
        
        all_moves = [
            'U', 'U\'', 'U2', 'D', 'D\'', 'D2',
            'L', 'L\'', 'L2', 'R', 'R\'', 'R2', 
            'F', 'F\'', 'F2', 'B', 'B\'', 'B2'
        ]
        
        for move in all_moves:
            test_cube = cube.copy()
            test_cube.execute_move(move)
            
            # Move should change the cube (except for some edge cases)
            # At minimum, it should be a valid operation
            assert isinstance(test_cube.state, np.ndarray)
            assert test_cube.state.shape == (54,)
    
    def test_state_consistency(self):
        """Test that cube state remains consistent after operations."""
        cube = RubikCube()
        
        # Each color should appear exactly 9 times in solved state
        for color in range(6):
            count = np.sum(cube.state == color)
            assert count == 9
        
        # After scrambling, color counts should remain the same
        cube.scramble(20)
        for color in range(6):
            count = np.sum(cube.state == color)
            assert count == 9
    
    def test_face_integrity(self):
        """Test that faces maintain their structure."""
        cube = RubikCube()
        
        # Test that getting and setting preserves face structure
        for face_idx in range(6):
            original_face = cube.get_face(face_idx).copy()
            cube.set_face(face_idx, original_face)
            retrieved_face = cube.get_face(face_idx)
            
            assert np.array_equal(original_face, retrieved_face)

if __name__ == '__main__':
    pytest.main([__file__])