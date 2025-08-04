"""
Move Engine - Handles all cube move operations
Implements the 18 standard Rubik's Cube moves.
"""

import numpy as np
from typing import List, Dict, Callable

class MoveEngine:
    """
    Handles all move operations for a Rubik's Cube.
    Implements efficient move transformations using numpy operations.
    """
    
    def __init__(self):
        """Initialize the move engine with all move definitions."""
        self.moves: Dict[str, Callable] = {
            'U': self._move_U, 'U\'': self._move_U_prime, 'U2': self._move_U2,
            'D': self._move_D, 'D\'': self._move_D_prime, 'D2': self._move_D2,
            'L': self._move_L, 'L\'': self._move_L_prime, 'L2': self._move_L2,
            'R': self._move_R, 'R\'': self._move_R_prime, 'R2': self._move_R2,
            'F': self._move_F, 'F\'': self._move_F_prime, 'F2': self._move_F2,
            'B': self._move_B, 'B\'': self._move_B_prime, 'B2': self._move_B2
        }
    
    def get_all_moves(self) -> List[str]:
        """Get list of all valid moves."""
        return list(self.moves.keys())
    
    def is_valid_move(self, move: str) -> bool:
        """Check if a move is valid."""
        return move in self.moves
    
    def apply_move(self, state: np.ndarray, move: str) -> np.ndarray:
        """Apply a move to a cube state and return the new state."""
        if not self.is_valid_move(move):
            raise ValueError(f"Invalid move: {move}")
        
        new_state = state.copy()
        self.moves[move](new_state)
        return new_state
    
    def _rotate_face_clockwise(self, state: np.ndarray, face_idx: int) -> None:
        """Rotate a face 90 degrees clockwise in-place."""
        face_start = face_idx * 9
        face = state[face_start:face_start + 9].reshape(3, 3)
        rotated = np.rot90(face, -1)  # -1 for clockwise
        state[face_start:face_start + 9] = rotated.flatten()
    
    def _rotate_face_counterclockwise(self, state: np.ndarray, face_idx: int) -> None:
        """Rotate a face 90 degrees counterclockwise in-place."""
        face_start = face_idx * 9
        face = state[face_start:face_start + 9].reshape(3, 3)
        rotated = np.rot90(face, 1)  # 1 for counterclockwise
        rotated = np.rot90(face, 1)  # 1 for counterclockwise
        state[face_start:face_start + 9] = rotated.flatten()
    
    # U moves (Up face)
    def _move_U(self, state: np.ndarray) -> None:
        """Up face clockwise rotation."""
        self._rotate_face_clockwise(state, 4)  # Up face
        # Cycle adjacent edges: Front → Right → Back → Left → Front
        temp = state[0:3].copy()
        state[0:3] = state[27:30]    # Left → Front
        state[27:30] = state[18:21]  # Back → Left
        state[18:21] = state[9:12]   # Right → Back
        state[9:12] = temp           # Front → Right
    
    def _move_U_prime(self, state: np.ndarray) -> None:
        """Up face counterclockwise rotation."""
        self._rotate_face_counterclockwise(state, 4)
        # Reverse of U move
        temp = state[0:3].copy()
        state[0:3] = state[9:12]     # Right → Front
        state[9:12] = state[18:21]   # Back → Right
        state[18:21] = state[27:30]  # Left → Back
        state[27:30] = temp          # Front → Left
    
    def _move_U2(self, state: np.ndarray) -> None:
        """Up face 180 degrees."""
        self._move_U(state)
        self._move_U(state)
    
    # D moves (Down face)
    def _move_D(self, state: np.ndarray) -> None:
        """Down face clockwise rotation."""
        self._rotate_face_clockwise(state, 5)  # Down face
        temp = state[6:9].copy()
        state[6:9] = state[15:18]    # Right → Front
        state[15:18] = state[24:27]  # Back → Right
        state[24:27] = state[33:36]  # Left → Back
        state[33:36] = temp          # Front → Left
    
    def _move_D_prime(self, state: np.ndarray) -> None:
        """Down face counterclockwise rotation."""
        self._rotate_face_counterclockwise(state, 5)
        temp = state[6:9].copy()
        state[6:9] = state[33:36]    # Left → Front
        state[33:36] = state[24:27]  # Back → Left
        state[24:27] = state[15:18]  # Right → Back
        state[15:18] = temp          # Front → Right
    
    def _move_D2(self, state: np.ndarray) -> None:
        """Down face 180 degrees."""
        self._move_D(state)
        self._move_D(state)
    
    # L moves (Left face)
    def _move_L(self, state: np.ndarray) -> None:
        """Left face clockwise rotation."""
        self._rotate_face_clockwise(state, 3)  # Left face
        temp = np.array([state[0], state[3], state[6]])
        state[[0, 3, 6]] = [state[45], state[48], state[51]]      # Down → Front
        state[[45, 48, 51]] = [state[24], state[21], state[18]]  # Back → Down
        state[[24, 21, 18]] = [state[36], state[39], state[42]]  # Up → Back
        state[[36, 39, 42]] = temp                               # Front → Up
    
    def _move_L_prime(self, state: np.ndarray) -> None:
        """Left face counterclockwise rotation."""
        self._rotate_face_counterclockwise(state, 3)
        temp = np.array([state[0], state[3], state[6]])
        state[[0, 3, 6]] = [state[36], state[39], state[42]]     # Up → Front
        state[[36, 39, 42]] = [state[24], state[21], state[18]] # Back → Up
        state[[24, 21, 18]] = [state[45], state[48], state[51]] # Down → Back
        state[[45, 48, 51]] = temp                              # Front → Down
    
    def _move_L2(self, state: np.ndarray) -> None:
        """Left face 180 degrees."""
        self._move_L(state)
        self._move_L(state)
    
    # R moves (Right face)
    def _move_R(self, state: np.ndarray) -> None:
        """Right face clockwise rotation."""
        self._rotate_face_clockwise(state, 1)  # Right face
        temp = np.array([state[2], state[5], state[8]])
        state[[2, 5, 8]] = [state[38], state[41], state[44]]     # Up → Front
        state[[38, 41, 44]] = [state[20], state[23], state[26]] # Back → Up
        state[[20, 23, 26]] = [state[47], state[50], state[53]] # Down → Back
        state[[47, 50, 53]] = temp                              # Front → Down
    
    def _move_R_prime(self, state: np.ndarray) -> None:
        """Right face counterclockwise rotation."""
        self._rotate_face_counterclockwise(state, 1)
        temp = np.array([state[2], state[5], state[8]])
        state[[2, 5, 8]] = [state[47], state[50], state[53]]    # Down → Front
        state[[47, 50, 53]] = [state[20], state[23], state[26]] # Back → Down
        state[[20, 23, 26]] = [state[38], state[41], state[44]] # Up → Back
        state[[38, 41, 44]] = temp                              # Front → Up
    
    def _move_R2(self, state: np.ndarray) -> None:
        """Right face 180 degrees."""
        self._move_R(state)
        self._move_R(state)
    
    # F moves (Front face)
    def _move_F(self, state: np.ndarray) -> None:
        """Front face clockwise rotation."""
        self._rotate_face_clockwise(state, 0)  # Front face
        
        # Save positions that will be overwritten
        temp = np.array([state[42], state[43], state[44]])  # Up bottom row
        
        # Rotate edge pieces clockwise around Front face
        # Up bottom → Right left column
        state[42], state[43], state[44] = state[35], state[32], state[29]  # Up ← Left (reversed order)
        # Left right column → Down top row  
        state[35], state[32], state[29] = state[47], state[46], state[45]  # Left ← Down
        # Down top row → Right left column
        state[47], state[46], state[45] = state[9], state[12], state[15]  # Down ← Right
        # Right left column → Up bottom row
        state[9], state[12], state[15] = temp[2], temp[1], temp[0]  # Right ← Up (reversed order)

    def _move_F_prime(self, state: np.ndarray) -> None:
        """Front face counterclockwise rotation."""
        self._rotate_face_counterclockwise(state, 0)
        
        # Save positions that will be overwritten  
        temp = np.array([state[42], state[43], state[44]])  # Up bottom row
        
        # Rotate edge pieces counterclockwise around Front face
        # Up bottom → Right left column (reversed order)
        state[42], state[43], state[44] = state[9], state[12], state[15]  # Up ← Right
        # Right left column → Down top row
        state[9], state[12], state[15] = state[47], state[46], state[45]  # Right ← Down
        # Down top row → Left right column
        state[47], state[46], state[45] = state[35], state[32], state[29]  # Down ← Left
        # Left right column → Up bottom row (reversed order)
        state[35], state[32], state[29] = temp[2], temp[1], temp[0]  # Left ← Up

    def _move_F2(self, state: np.ndarray) -> None:
        """Front face 180 degrees."""
        self._move_F(state)
        self._move_F(state)
    
    # B moves (Back face)
    def _move_B(self, state: np.ndarray) -> None:
        """Back face clockwise rotation."""
        self._rotate_face_clockwise(state, 2)  # Back face
        temp = np.array([state[0], state[1], state[2]])
        state[[0, 1, 2]] = [state[9], state[10], state[11]]     # Right → Front top
        state[[9, 10, 11]] = [state[53], state[52], state[51]]  # Down → Right right
        state[[53, 52, 51]] = [state[35], state[34], state[33]] # Left → Down bottom
        state[[35, 34, 33]] = temp                              # Front top → Left left
    
    def _move_B_prime(self, state: np.ndarray) -> None:
        """Back face counterclockwise rotation."""
        self._rotate_face_counterclockwise(state, 2)
        temp = np.array([state[0], state[1], state[2]])
        state[[0, 1, 2]] = [state[35], state[34], state[33]]    # Left → Front top
        state[[35, 34, 33]] = [state[53], state[52], state[51]] # Down → Left left
        state[[53, 52, 51]] = [state[9], state[10], state[11]]  # Right → Down bottom
        state[[9, 10, 11]] = temp                               # Front top → Right right
    
    def _move_B2(self, state: np.ndarray) -> None:
        """Back face 180 degrees."""
        self._move_B(state)
        self._move_B(state)


