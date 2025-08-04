"""
Heuristic Functions for Rubik's Cube Solving
"""

import numpy as np
from typing import Dict, List, Tuple
from ..core.cube import RubikCube

class Heuristics:
    """
    Collection of heuristic functions for guiding the search algorithm.
    """
    
    def __init__(self):
        """Initialize heuristic calculator with precomputed data."""
        self._init_piece_positions()
    
    def _init_piece_positions(self) -> None:
        """Initialize piece position mappings for advanced heuristics."""
        # Corner positions (each corner has 3 facelets)
        self.corners = [
            [0, 9, 36],   # Front-Right-Up
            [2, 11, 38],  # Front-Right-Down  
            [6, 15, 42],  # Front-Left-Up
            [8, 17, 44],  # Front-Left-Down
            [18, 27, 45], # Back-Left-Up
            [20, 29, 47], # Back-Left-Down
            [24, 33, 51], # Back-Right-Up
            [26, 35, 53]  # Back-Right-Down
        ]
        
        # Edge positions (each edge has 2 facelets)
        self.edges = [
            [1, 37], [3, 39], [5, 41], [7, 43],      # Up ring
            [10, 46], [12, 48], [14, 50], [16, 52],  # Down ring
            [19, 28], [21, 30], [23, 32], [25, 34]   # Middle ring
        ]
        
        # Center positions (fixed in standard cube)
        self.centers = [4, 13, 22, 31, 40, 49]
    
    def manhattan_distance(self, cube: RubikCube) -> int:
        """
        Basic Manhattan distance heuristic.
        Counts misplaced facelets on each face.
        """
        solved_cube = RubikCube()
        distance = 0
        
        for face_idx in range(6):
            current_face = cube.get_face(face_idx)
            solved_face = solved_cube.get_face(face_idx)
            
            # Count misplaced pieces (excluding center)
            for i in range(3):
                for j in range(3):
                    if (i, j) != (1, 1):  # Skip center
                        if current_face[i, j] != solved_face[i, j]:
                            distance += 1
        
        return min(distance, 20) // 4  # Rough scaling factor
    
    def corner_edge_heuristic(self, cube: RubikCube) -> int:
        """
        Advanced heuristic considering corner and edge piece positions.
        More informed than Manhattan distance.
        """
        if cube.is_solved():
            return 0
            
        solved_cube = RubikCube()
        heuristic = 0
        
        # Check corners
        for corner in self.corners:
            current_colors = sorted([cube.state[pos] for pos in corner])
            solved_colors = sorted([solved_cube.state[pos] for pos in corner])
            
            if current_colors != solved_colors:
                heuristic += 2  # Corner piece out of place (reduced from 3)
            else:
                # Check orientation
                current_oriented = [cube.state[pos] for pos in corner]
                solved_oriented = [solved_cube.state[pos] for pos in corner]
                if current_oriented != solved_oriented:
                    heuristic += 1  # Corner twisted
        
        # Check edges  
        for edge in self.edges:
            current_colors = sorted([cube.state[pos] for pos in edge])
            solved_colors = sorted([solved_cube.state[pos] for pos in edge])
            
            if current_colors != solved_colors:
                heuristic += 1  # Edge piece out of place (reduced from 2)
            else:
                # Check orientation
                current_oriented = [cube.state[pos] for pos in edge]
                solved_oriented = [solved_cube.state[pos] for pos in edge]
                if current_oriented != solved_oriented:
                    heuristic += 1  # Edge flipped
        
        return max(1, heuristic // 4) if heuristic > 0 else 0  # More conservative scaling
    
    def layer_completion_heuristic(self, cube: RubikCube) -> int:
        """
        Heuristic based on layer completion progress.
        """
        solved_cube = RubikCube()
        heuristic = 0
        
        # Check bottom layer (Down face + adjacent bottom rows)
        bottom_positions = list(range(45, 54))  # Down face
        bottom_positions.extend([6, 7, 8, 15, 16, 17, 24, 25, 26, 33, 34, 35])
        
        bottom_solved = True
        for pos in bottom_positions:
            if cube.state[pos] != solved_cube.state[pos]:
                bottom_solved = False
                heuristic += 1
        
        if not bottom_solved:
            heuristic += 20  # Heavy penalty for incomplete bottom
        
        # Check middle layer
        if bottom_solved:
            middle_positions = [3, 5, 10, 12, 14, 16, 19, 21, 23, 25, 28, 30, 32, 34]
            for pos in middle_positions:
                if cube.state[pos] != solved_cube.state[pos]:
                    heuristic += 2
        
        return heuristic
    
    def combined_heuristic(self, cube: RubikCube) -> int:
        """
        Combined heuristic using multiple strategies.
        """
        h1 = self.manhattan_distance(cube)
        h2 = self.corner_edge_heuristic(cube) 
        h3 = self.layer_completion_heuristic(cube)
        
        # Weighted combination
        return int(0.3 * h1 + 0.5 * h2 + 0.2 * h3)
    
    def pattern_database_heuristic(self, cube: RubikCube) -> int:
        """
        Pattern database heuristic (simplified version).
        In a full implementation, this would use precomputed databases.
        """
        # This is a simplified version - a full implementation would
        # require extensive precomputation and storage
        
        # Count patterns in corners
        corner_pattern_score = 0
        solved_cube = RubikCube()
        
        for corner in self.corners:
            corner_colors = [cube.state[pos] for pos in corner]
            solved_colors = [solved_cube.state[pos] for pos in corner]
            
            # Simple pattern matching
            if corner_colors == solved_colors:
                corner_pattern_score += 0
            elif sorted(corner_colors) == sorted(solved_colors):
                corner_pattern_score += 1  # Right colors, wrong orientation
            else:
                corner_pattern_score += 3  # Wrong position
        
        return corner_pattern_score
    
    def estimate_moves_to_solve(self, cube: RubikCube) -> int:
        """
        Estimate minimum moves needed to solve the cube.
        This is the primary heuristic used by the solver.
        """
        return self.corner_edge_heuristic(cube)
