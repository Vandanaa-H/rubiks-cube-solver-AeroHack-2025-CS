"""
Utility functions for the solving algorithms
"""

import time
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class SearchStatistics:
    """Statistics tracking for search algorithms."""
    nodes_explored: int = 0
    solution_found: bool = False
    solution_length: int = 0
    solve_time: float = 0.0
    max_depth_reached: int = 0
    
    def reset(self) -> None:
        """Reset all statistics."""
        self.nodes_explored = 0
        self.solution_found = False
        self.solution_length = 0
        self.solve_time = 0.0
        self.max_depth_reached = 0
    
    def __str__(self) -> str:
        """String representation of statistics."""
        return (f"Nodes: {self.nodes_explored}, "
                f"Solution: {'Yes' if self.solution_found else 'No'}, "
                f"Length: {self.solution_length}, "
                f"Time: {self.solve_time:.2f}s")

class MoveOptimizer:
    """Optimizes move sequences by removing redundancies."""
    
    def __init__(self):
        """Initialize the move optimizer."""
        self.face_moves = {
            'U': ['U', 'U\'', 'U2'], 'D': ['D', 'D\'', 'D2'],
            'L': ['L', 'L\'', 'L2'], 'R': ['R', 'R\'', 'R2'],
            'F': ['F', 'F\'', 'F2'], 'B': ['B', 'B\'', 'B2']
        }
        
        self.move_values = {
            'U': 1, 'U\'': -1, 'U2': 2,
            'D': 1, 'D\'': -1, 'D2': 2,
            'L': 1, 'L\'': -1, 'L2': 2,
            'R': 1, 'R\'': -1, 'R2': 2,
            'F': 1, 'F\'': -1, 'F2': 2,
            'B': 1, 'B\'': -1, 'B2': 2
        }
    
    def optimize_sequence(self, moves: List[str]) -> List[str]:
        """
        Optimize a move sequence by combining redundant moves.
        
        Args:
            moves: List of moves to optimize
            
        Returns:
            Optimized move sequence
        """
        if not moves:
            return moves
        
        optimized = []
        i = 0
        
        while i < len(moves):
            current_move = moves[i]
            face = current_move[0]
            
            # Count consecutive moves on the same face
            consecutive_moves = [current_move]
            j = i + 1
            
            while j < len(moves) and moves[j][0] == face:
                consecutive_moves.append(moves[j])
                j += 1
            
            # Calculate net rotation
            net_rotation = sum(self.move_values[move] for move in consecutive_moves)
            net_rotation = net_rotation % 4
            
            # Add optimized move
            if net_rotation == 1:
                optimized.append(face)
            elif net_rotation == 2:
                optimized.append(face + '2')
            elif net_rotation == 3:
                optimized.append(face + '\'')
            # net_rotation == 0 means no move needed
            
            i = j
        
        return optimized
    
    def remove_redundant_patterns(self, moves: List[str]) -> List[str]:
        """
        Remove redundant move patterns like A B A -> B A B (if shorter).
        """
        if len(moves) < 3:
            return moves
        
        optimized = moves.copy()
        changed = True
        
        while changed:
            changed = False
            i = 0
            
            while i < len(optimized) - 2:
                # Look for A B A pattern
                if (optimized[i][0] == optimized[i + 2][0] and 
                    optimized[i][0] != optimized[i + 1][0]):
                    
                    # Try to optimize this pattern
                    # This is a simplified version - more complex optimizations possible
                    face_a = optimized[i][0]
                    face_b = optimized[i + 1][0]
                    
                    # For now, just remove obvious redundancies
                    if optimized[i] == optimized[i + 2]:
                        # A B A -> B (if A and A cancel out in this context)
                        optimized = optimized[:i] + optimized[i + 1:i + 2] + optimized[i + 3:]
                        changed = True
                        continue
                
                i += 1
        
        return optimized

class Timer:
    """Simple timer for performance measurement."""
    
    def __init__(self):
        """Initialize timer."""
        self.start_time = None
        self.end_time = None
    
    def start(self) -> None:
        """Start the timer."""
        self.start_time = time.time()
    
    def stop(self) -> float:
        """Stop the timer and return elapsed time."""
        self.end_time = time.time()
        if self.start_time is None:
            return 0.0
        return self.end_time - self.start_time
    
    def elapsed(self) -> float:
        """Get elapsed time without stopping."""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time

def format_move_sequence(moves: List[str], line_length: int = 50) -> str:
    """
    Format a move sequence for nice display.
    
    Args:
        moves: List of moves
        line_length: Maximum characters per line
        
    Returns:
        Formatted string
    """
    if not moves:
        return "No moves"
    
    result = []
    current_line = ""
    
    for move in moves:
        if len(current_line) + len(move) + 1 > line_length:
            result.append(current_line.strip())
            current_line = move + " "
        else:
            current_line += move + " "
    
    if current_line.strip():
        result.append(current_line.strip())
    
    return "\n".join(result)

def analyze_move_sequence(moves: List[str]) -> Dict[str, int]:
    """
    Analyze a move sequence and return statistics.
    
    Args:
        moves: List of moves to analyze
        
    Returns:
        Dictionary with analysis results
    """
    if not moves:
        return {"total_moves": 0}
    
    analysis = {
        "total_moves": len(moves),
        "unique_moves": len(set(moves)),
        "face_distribution": {},
        "move_type_distribution": {"quarter": 0, "half": 0, "prime": 0}
    }
    
    # Count face distribution
    for move in moves:
        face = move[0]
        analysis["face_distribution"][face] = analysis["face_distribution"].get(face, 0) + 1
    
    # Count move types
    for move in moves:
        if move.endswith('2'):
            analysis["move_type_distribution"]["half"] += 1
        elif move.endswith('\''):
            analysis["move_type_distribution"]["prime"] += 1
        else:
            analysis["move_type_distribution"]["quarter"] += 1
    
    return analysis