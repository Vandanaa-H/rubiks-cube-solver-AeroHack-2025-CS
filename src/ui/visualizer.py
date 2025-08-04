"""
Cube Visualizer - Advanced visualization for Rubik's Cube
Provides 2D and 3D-like representations of the cube state.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple, Optional
from ..core.cube import RubikCube

class CubeVisualizer:
    """
    Advanced visualizer for Rubik's Cube with multiple display modes.
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        # Color mapping for matplotlib
        self.color_map = {
            0: '#FFFFFF',  # White
            1: '#FF0000',  # Red  
            2: '#0000FF',  # Blue
            3: '#FFA500',  # Orange
            4: '#00FF00',  # Green
            5: '#FFFF00'   # Yellow
        }
        
        self.color_names = ['White', 'Red', 'Blue', 'Orange', 'Green', 'Yellow']
        
        # Text symbols for console display
        self.text_symbols = {
            0: '⬜', 1: '🟥', 2: '🟦', 3: '🟧', 4: '🟩', 5: '🟨'
        }
        
        # ASCII art symbols
        self.ascii_symbols = {
            0: 'W', 1: 'R', 2: 'B', 3: 'O', 4: 'G', 5: 'Y'
        }
    
    def display_2d_net(self, cube: RubikCube, title: str = "Rubik's Cube State") -> None:
        """
        Display cube as 2D net using matplotlib.
        
        Args:
            cube: The cube to visualize
            title: Title for the plot
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 9))
        
        # Define positions for the net layout
        # Layout:
        #     [U]
        # [L] [F] [R] [B]
        #     [D]
        
        positions = {
            4: (1, 2),  # Up
            3: (0, 1),  # Left  
            0: (1, 1),  # Front
            1: (2, 1),  # Right
            2: (3, 1),  # Back
            5: (1, 0)   # Down
        }
        
        square_size = 0.3
        gap = 0.05
        
        for face_idx, (x_offset, y_offset) in positions.items():
            face = cube.get_face(face_idx)
            
            for i in range(3):
                for j in range(3):
                    color = self.color_map[face[i, j]]
                    
                    x = x_offset + j * (square_size + gap)
                    y = y_offset + (2 - i) * (square_size + gap)  # Flip y for correct orientation
                    
                    rect = patches.Rectangle(
                        (x, y), square_size, square_size,
                        linewidth=2, edgecolor='black', facecolor=color
                    )
                    ax.add_patch(rect)
                    
                    # Add text label
                    ax.text(x + square_size/2, y + square_size/2, 
                           self.ascii_symbols[face[i, j]], 
                           ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Add face labels
        label_positions = {
            'U': (1.45, 2.9), 'L': (0.45, 1.9), 'F': (1.45, 1.9),
            'R': (2.45, 1.9), 'B': (3.45, 1.9), 'D': (1.45, 0.9)
        }
        
        for label, (x, y) in label_positions.items():
            ax.text(x, y, label, ha='center', va='center', fontsize=14, fontweight='bold')
        
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def display_ascii_art(self, cube: RubikCube) -> str:
        """
        Generate ASCII art representation of the cube.
        
        Args:
            cube: The cube to visualize
            
        Returns:
            ASCII art string
        """
        faces = [cube.get_face(i) for i in range(6)]
        
        # Convert to ASCII symbols
        ascii_faces = []
        for face in faces:
            ascii_face = []
            for row in face:
                ascii_row = [self.ascii_symbols[cell] for cell in row]
                ascii_face.append(ascii_row)
            ascii_faces.append(ascii_face)
        
        # Build the net layout
        lines = []
        
        # Top face (Up)
        lines.append("      " + " ".join(ascii_faces[4][0]))
        lines.append("      " + " ".join(ascii_faces[4][1]))
        lines.append("      " + " ".join(ascii_faces[4][2]))
        lines.append("")
        
        # Middle row (Left, Front, Right, Back)
        for i in range(3):
            line = " ".join(ascii_faces[3][i]) + " "  # Left
            line += " ".join(ascii_faces[0][i]) + " "  # Front
            line += " ".join(ascii_faces[1][i]) + " "  # Right
            line += " ".join(ascii_faces[2][i])       # Back
            lines.append(line)
        
        lines.append("")
        
        # Bottom face (Down)
        lines.append("      " + " ".join(ascii_faces[5][0]))
        lines.append("      " + " ".join(ascii_faces[5][1]))
        lines.append("      " + " ".join(ascii_faces[5][2]))
        
        return "\n".join(lines)
    
    def display_detailed_console(self, cube: RubikCube) -> None:
        """
        Display detailed console representation with colors and labels.
        
        Args:
            cube: The cube to visualize
        """
        print("╔" + "═" * 50 + "╗")
        print("║" + " " * 15 + "CUBE STATE DETAIL" + " " * 15 + "║")
        print("╚" + "═" * 50 + "╝")
        
        face_names = ['Front', 'Right', 'Back', 'Left', 'Up', 'Down']
        face_colors = ['White', 'Red', 'Blue', 'Orange', 'Green', 'Yellow']
        
        for i, (face_name, target_color) in enumerate(zip(face_names, face_colors)):
            face = cube.get_face(i)
            print(f"\n{face_name} Face (Target: {target_color}):")
            print("┌" + "─" * 7 + "┐")
            
            for row in face:
                symbols = [self.text_symbols[cell] for cell in row]
                print("│ " + " ".join(symbols) + " │")
            
            print("└" + "─" * 7 + "┘")
            
            # Show face statistics
            correct_count = np.sum(face == i)
            print(f"Correct pieces: {correct_count}/9")
    
    def display_move_animation_frames(self, cube: RubikCube, moves: List[str]) -> List[str]:
        """
        Generate animation frames for a sequence of moves.
        
        Args:
            cube: Starting cube state
            moves: Sequence of moves to animate
            
        Returns:
            List of ASCII art frames
        """
        frames = []
        current_cube = cube.copy()
        
        # Initial frame
        frames.append(self.display_ascii_art(current_cube))
        
        # Frame for each move
        for move in moves:
            current_cube.execute_move(move)
            frame = self.display_ascii_art(current_cube)
            frames.append(frame)
        
        return frames
    
    def save_state_image(self, cube: RubikCube, filename: str, title: str = None) -> None:
        """
        Save cube state as image file.
        
        Args:
            cube: The cube to save
            filename: Output filename
            title: Optional title for the image
        """
        if title is None:
            title = f"Cube State - {'Solved' if cube.is_solved() else 'Scrambled'}"
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 9))
        
        # Use the same 2D net display logic
        positions = {
            4: (1, 2),  # Up
            3: (0, 1),  # Left  
            0: (1, 1),  # Front
            1: (2, 1),  # Right
            2: (3, 1),  # Back
            5: (1, 0)   # Down
        }
        
        square_size = 0.3
        gap = 0.05
        
        for face_idx, (x_offset, y_offset) in positions.items():
            face = cube.get_face(face_idx)
            
            for i in range(3):
                for j in range(3):
                    color = self.color_map[face[i, j]]
                    
                    x = x_offset + j * (square_size + gap)
                    y = y_offset + (2 - i) * (square_size + gap)
                    
                    rect = patches.Rectangle(
                        (x, y), square_size, square_size,
                        linewidth=2, edgecolor='black', facecolor=color
                    )
                    ax.add_patch(rect)
                    
                    ax.text(x + square_size/2, y + square_size/2, 
                           self.ascii_symbols[face[i, j]], 
                           ha='center', va='center', fontsize=12, fontweight='bold')
        
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def compare_states(self, cube1: RubikCube, cube2: RubikCube, 
                      labels: Tuple[str, str] = ("State 1", "State 2")) -> None:
        """
        Display two cube states side by side for comparison.
        
        Args:
            cube1: First cube state
            cube2: Second cube state
            labels: Labels for the two states
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9))
        
        # Display first cube
        self._plot_cube_on_axis(ax1, cube1, labels[0])
        
        # Display second cube
        self._plot_cube_on_axis(ax2, cube2, labels[1])
        
        plt.tight_layout()
        plt.show()
    
    def _plot_cube_on_axis(self, ax, cube: RubikCube, title: str) -> None:
        """Helper method to plot cube on specific axis."""
        positions = {
            4: (1, 2),  # Up
            3: (0, 1),  # Left  
            0: (1, 1),  # Front
            1: (2, 1),  # Right
            2: (3, 1),  # Back
            5: (1, 0)   # Down
        }
        
        square_size = 0.3
        gap = 0.05
        
        for face_idx, (x_offset, y_offset) in positions.items():
            face = cube.get_face(face_idx)
            
            for i in range(3):
                for j in range(3):
                    color = self.color_map[face[i, j]]
                    
                    x = x_offset + j * (square_size + gap)
                    y = y_offset + (2 - i) * (square_size + gap)
                    
                    rect = patches.Rectangle(
                        (x, y), square_size, square_size,
                        linewidth=2, edgecolor='black', facecolor=color
                    )
                    ax.add_patch(rect)
                    
                    ax.text(x + square_size/2, y + square_size/2, 
                           self.ascii_symbols[face[i, j]], 
                           ha='center', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=14, fontweight='bold')
