"""
Rubik's Cube Core Representation
Handles cube state management and basic operations.
"""

import numpy as np
from typing import List, Optional
from .moves import MoveEngine

class RubikCube:
    """
    Represents a 3x3 Rubik's Cube with state management and move operations.
    Uses flattened array representation for 54 facelets (6 faces × 9 squares).
    
    Face Layout:
    - Face 0: Front (White)   - indices 0-8
    - Face 1: Right (Red)     - indices 9-17  
    - Face 2: Back (Blue)     - indices 18-26
    - Face 3: Left (Orange)   - indices 27-35
    - Face 4: Up (Green)      - indices 36-44
    - Face 5: Down (Yellow)   - indices 45-53
    """
    
    # Color constants
    WHITE, RED, BLUE, ORANGE, GREEN, YELLOW = range(6)
    COLOR_NAMES = ['White', 'Red', 'Blue', 'Orange', 'Green', 'Yellow']
    COLOR_SYMBOLS = ['⬜', '🟥', '🟦', '🟧', '🟩', '🟨']
    
    def __init__(self, state: Optional[np.ndarray] = None):
        """Initialize cube with given state or solved state."""
        if state is not None:
            state = np.array(state)  # Convert to numpy array if needed
            if len(state) != 54:
                raise ValueError("State must have exactly 54 elements")
            self.state = state.copy()
        else:
            self.state = self._create_solved_state()
        
        self.move_history: List[str] = []
        self.move_count: int = 0
        self.move_engine = MoveEngine()
    
    def _create_solved_state(self) -> np.ndarray:
        """Create a solved cube state with proper color arrangement."""
        state = np.zeros(54, dtype=int)
        for face in range(6):
            for square in range(9):
                state[face * 9 + square] = face
        return state
    
    def get_face(self, face_idx: int) -> np.ndarray:
        """Get a specific face as a 3x3 array."""
        if not 0 <= face_idx < 6:
            raise ValueError("Face index must be between 0 and 5")
        return self.state[face_idx * 9:(face_idx + 1) * 9].reshape(3, 3)
    
    def set_face(self, face_idx: int, face_data: np.ndarray) -> None:
        """Set a specific face from a 3x3 array."""
        if not 0 <= face_idx < 6:
            raise ValueError("Face index must be between 0 and 5")
        if face_data.shape != (3, 3):
            raise ValueError("Face data must be a 3x3 array")
        self.state[face_idx * 9:(face_idx + 1) * 9] = face_data.flatten()
    
    def execute_move(self, move: str) -> None:
        """Execute a single move on the cube."""
        if not isinstance(move, str):
            raise ValueError(f"Move must be a string, got {type(move)}")
        if not self.move_engine.is_valid_move(move):
            raise ValueError(f"Invalid move: {move}")
        
        self.state = self.move_engine.apply_move(self.state, move)
        self.move_history.append(move)
        self.move_count += 1
    
    def execute_sequence(self, moves: List[str]) -> None:
        """Execute a sequence of moves."""
        for move in moves:
            self.execute_move(move)
    
    def is_solved(self) -> bool:
        """Check if the cube is in solved state."""
        solved_state = self._create_solved_state()
        return np.array_equal(self.state, solved_state)
    
    def scramble(self, num_moves: int = 20, seed: Optional[int] = None) -> List[str]:
        """
        Scramble the cube with random moves.
        Returns the list of moves used for scrambling.
        """
        if seed is not None:
            np.random.seed(seed)
        
        moves = self.move_engine.get_all_moves()
        scramble_moves = []
        last_move = None
        
        for _ in range(num_moves):
            # Get valid moves (avoid immediate reverses)
            valid_moves = [m for m in moves if not self._is_reverse_move(m, last_move)]
            move = np.random.choice(valid_moves)
            
            self.execute_move(move)
            scramble_moves.append(move)
            last_move = move
        
        return scramble_moves
    
    def _is_reverse_move(self, move1: str, move2: str) -> bool:
        """Check if move1 is the reverse of move2."""
        if move2 is None:
            return False
        
        reverse_map = {
            'U': 'U\'', 'U\'': 'U', 'U2': 'U2',
            'D': 'D\'', 'D\'': 'D', 'D2': 'D2',
            'L': 'L\'', 'L\'': 'L', 'L2': 'L2',
            'R': 'R\'', 'R\'': 'R', 'R2': 'R2',
            'F': 'F\'', 'F\'': 'F', 'F2': 'F2',
            'B': 'B\'', 'B\'': 'B', 'B2': 'B2'
        }
        
        return move1 == reverse_map.get(move2, '')
    
    def copy(self) -> 'RubikCube':
        """Create a deep copy of the cube."""
        new_cube = RubikCube(self.state)
        new_cube.move_history = self.move_history.copy()
        return new_cube
    
    def get_state_string(self) -> str:
        """Get a string representation of the cube state for hashing."""
        return ''.join(map(str, self.state))
    
    def reset(self) -> None:
        """Reset cube to solved state."""
        self.state = self._create_solved_state()
        self.move_history.clear()
    
    def get_move_count(self) -> int:
        """Get the number of moves executed."""
        return len(self.move_history)
    
    def __str__(self) -> str:
        """String representation of the cube for display."""
        result = []
        face_names = ['Front', 'Right', 'Back', 'Left', 'Up', 'Down']
        
        for i, face_name in enumerate(face_names):
            face = self.get_face(i)
            result.append(f"{face_name} ({self.COLOR_NAMES[i]}):")
            for row in face:
                symbols = [self.COLOR_SYMBOLS[cell] for cell in row]
                result.append(' '.join(symbols))
            result.append('')
        
        return '\n'.join(result)
    
    def __eq__(self, other: 'RubikCube') -> bool:
        """Check equality with another cube."""
        return np.array_equal(self.state, other.state)
    
    def __hash__(self) -> int:
        """Hash function for use in sets and dictionaries."""
        return hash(self.get_state_string())

