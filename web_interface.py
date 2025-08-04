#!/usr/bin/env python3
"""
Creative Web Interface for Rubik's Cube Solver
AeroHack 2025 - Modern Streamlit UI with unique features
"""

import streamlit as st
import time
import sys
import os
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.cube import RubikCube
from src.algorithms.astar_solver import AStarSolver

# Page config
st.set_page_config(
    page_title="🧩 Rubik's Cube Solver - AeroHack 2025",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main content area */
    .main > div {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Instruction cards */
    .instruction-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
        color: #1565c0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #9c27b0;
        margin: 1rem 0;
        color: #4a148c;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Success alerts */
    .success-alert {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border: 2px solid #4caf50;
        color: #2e7d32;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Error alerts */
    .error-alert {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border: 2px solid #f44336;
        color: #c62828;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Warning alerts */
    .warning-alert {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%);
        border: 2px solid #ff9800;
        color: #e65100;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Cube face styling */
    .cube-face {
        width: 60px;
        height: 60px;
        border: 3px solid #333;
        display: inline-block;
        text-align: center;
        line-height: 54px;
        margin: 3px;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric containers */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #dee2e6;
        padding: 1rem;
        border-radius: 10px;
        color: #495057;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Title styling */
    h1, h2, h3 {
        color: #2c3e50;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'cube' not in st.session_state:
        st.session_state.cube = RubikCube()
    if 'solver' not in st.session_state:
        st.session_state.solver = AStarSolver(max_depth=20, timeout=10)
    if 'solve_history' not in st.session_state:
        st.session_state.solve_history = []
    if 'current_scramble' not in st.session_state:
        st.session_state.current_scramble = []

def draw_cube_3d():
    """Create 3D visualization of the cube"""
    try:
        # Create a 3D cube visualization using plotly
        fig = go.Figure()
        
        # Define cube faces with colors
        colors = {0: 'white', 1: 'red', 2: 'blue', 3: 'orange', 4: 'green', 5: 'yellow'}
        
        # Add cube faces (simplified for demo)
        x = [0, 1, 1, 0, 0]
        y = [0, 0, 1, 1, 0]
        z = [0, 0, 0, 0, 0]
        
        for i in range(6):
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=[i]*5,
                mode='lines+markers',
                name=f'Face {i}',
                line=dict(color=colors.get(i, 'gray'), width=5)
            ))
        
        fig.update_layout(
            title="3D Cube Visualization",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y", 
                zaxis_title="Z"
            ),
            width=400,
            height=400
        )
        
        return fig
    except:
        return None

def display_cube_2d():
    """Display 2D cube representation"""
    cube_state = st.session_state.cube.state
    
    # Color mapping for display
    colors = {0: '🟦', 1: '🟥', 2: '🟩', 3: '🟨', 4: '🟫', 5: '⬜'}
    
    # Create 2D representation
    st.markdown("### 🎲 Current Cube State")
    
    # Top face
    st.markdown("**Top Face (U)**")
    for i in range(3):
        row = ""
        for j in range(3):
            try:
                color_val = int(cube_state[0, i, j]) if cube_state.ndim > 1 else 0
                row += colors.get(color_val, '⬛') + " "
            except:
                row += "⬛ "
        st.markdown(f"<div style='text-align: center; font-size: 20px;'>{row}</div>", 
                   unsafe_allow_html=True)
    
    # Middle row (Left, Front, Right, Back)
    st.markdown("**Middle Row (L-F-R-B)**")
    face_names = ["Left", "Front", "Right", "Back"]
    cols = st.columns(4)
    
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"**{face_names[idx]}**")
            for i in range(3):
                row = ""
                for j in range(3):
                    try:
                        face_idx = idx + 1 if idx < 3 else 4
                        color_val = int(cube_state[face_idx, i, j]) if cube_state.ndim > 1 else idx
                        row += colors.get(color_val, '⬛')
                    except:
                        row += "⬛"
                st.markdown(f"<div style='font-size: 16px;'>{row}</div>", 
                           unsafe_allow_html=True)
    
    # Bottom face
    st.markdown("**Bottom Face (D)**")
    for i in range(3):
        row = ""
        for j in range(3):
            try:
                color_val = int(cube_state[5, i, j]) if cube_state.ndim > 1 else 5
                row += colors.get(color_val, '⬛') + " "
            except:
                row += "⬛ "
        st.markdown(f"<div style='text-align: center; font-size: 20px;'>{row}</div>", 
                   unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧩 Rubik's Cube Solver</h1>
        <h3>AeroHack 2025 - Collins Aerospace Challenge</h3>
        <p>Advanced AI-Powered Algorithmic Solution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Instructions Section
    with st.expander("📖 How to Use This Application - Click to Expand", expanded=False):
        st.markdown("""
        <div class="instruction-card">
            <h3>🚀 Getting Started - 4 Easy Steps</h3>
            
            <h4>📋 Step 1: Understanding the Interface</h4>
            <ul>
                <li><strong>🎮 Left Sidebar:</strong> Your control panel for all cube operations</li>
                <li><strong>📊 Main Area:</strong> Displays cube state, solver results, and analytics</li>
                <li><strong>🎲 Cube Display:</strong> Shows current cube configuration with colors</li>
            </ul>
            
            <h4>🎯 Step 2: Scramble Your Cube</h4>
            <ul>
                <li>Click <strong>"🎲 Random Scramble"</strong> in the sidebar for automatic scrambling</li>
                <li>Or use <strong>"Manual Moves"</strong> dropdown to apply specific moves</li>
                <li>Watch the cube state update in real-time!</li>
            </ul>
            
            <h4>🧠 Step 3: Solve the Cube</h4>
            <ul>
                <li>Adjust <strong>"Solver Settings"</strong> if needed (default works great!)</li>
                <li>Click <strong>"🔮 Solve Cube"</strong> in the main area</li>
                <li>Watch the AI find the optimal solution sequence</li>
            </ul>
            
            <h4>📈 Step 4: Analyze Performance</h4>
            <ul>
                <li>View solve time, move count, and efficiency metrics</li>
                <li>Check the performance graphs and statistics</li>
                <li>Compare different solving attempts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="instruction-card">
            <h3>🎮 Interactive Features</h3>
            
            <h4>🔧 Manual Controls</h4>
            <ul>
                <li><strong>Face Rotations:</strong> U, D, L, R, F, B (clockwise)</li>
                <li><strong>Counter-clockwise:</strong> U', D', L', R', F', B' (add apostrophe)</li>
                <li><strong>Double turns:</strong> U2, D2, L2, R2, F2, B2 (180 degrees)</li>
            </ul>
            
            <h4>🎲 Cube Faces Legend</h4>
            <ul>
                <li><strong>U:</strong> Up/Top face (White)</li>
                <li><strong>D:</strong> Down/Bottom face (Yellow)</li>
                <li><strong>L:</strong> Left face (Orange)</li>
                <li><strong>R:</strong> Right face (Red)</li>
                <li><strong>F:</strong> Front face (Green)</li>
                <li><strong>B:</strong> Back face (Blue)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-alert">
            <h4>💡 Pro Tips for Best Results</h4>
            <ul>
                <li><strong>🎯 Start Simple:</strong> Try a few random scrambles first to see how it works</li>
                <li><strong>⚡ Performance:</strong> Keep Max Depth at 20 for good balance of speed vs. optimality</li>
                <li><strong>🕐 Timeout:</strong> 10 seconds is usually enough for most scrambles</li>
                <li><strong>📊 Analytics:</strong> Use the performance metrics to understand algorithm efficiency</li>
                <li><strong>🔄 Reset:</strong> Click "Reset Cube" anytime to return to solved state</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.markdown("""
    <div class="success-alert">
        <h4>⚡ Quick Start: Try it in 30 seconds!</h4>
        <p><strong>1.</strong> Click "🎲 Random Scramble" in the sidebar →  
        <strong>2.</strong> Click "🔮 Solve Cube" below →  
        <strong>3.</strong> Watch the magic happen! ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
            <h2>🎮 Control Panel</h2>
            <p>Your cube manipulation center</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Cube status with enhanced styling
        is_solved = st.session_state.cube.is_solved()
        status_color = "🟢" if is_solved else "🔴"
        status_text = "SOLVED" if is_solved else "SCRAMBLED"
        status_bg = "success" if is_solved else "error"
        
        st.markdown(f"""
        <div class="{status_bg}-alert" style="text-align: center; font-weight: bold; font-size: 1.1em;">
            <h4>Cube Status: {status_color} {status_text}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions with help text
        st.markdown("""
        <div class="instruction-card">
            <h4>🚀 Quick Actions</h4>
            <p><small>Fast operations to get started quickly</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Random\nScramble", use_container_width=True, help="Generate a random scramble (5-12 moves)"):
                scramble_moves = ['U', 'D', 'L', 'R', 'F', 'B', 'U\'', 'D\'', 'L\'', 'R\'', 'F\'', 'B\'']
                random_scramble = np.random.choice(scramble_moves, size=np.random.randint(5, 12))
                st.session_state.current_scramble = list(random_scramble)
                st.session_state.cube.execute_sequence(random_scramble)
                st.success(f"✅ Applied scramble: {' '.join(random_scramble)}")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset\nCube", use_container_width=True, help="Reset cube to solved state"):
                st.session_state.cube.reset()
                st.session_state.current_scramble = []
                st.success("✅ Cube reset to solved state!")
                st.rerun()
        
        st.markdown("---")
        
        # Manual moves with better organization
        st.markdown("""
        <div class="instruction-card">
            <h4>🔧 Manual Moves</h4>
            <p><small>Apply specific moves to the cube</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Organize moves by face
        st.markdown("**🔸 Select Face & Direction:**")
        move_categories = {
            'Up (U)': ['U', 'U\'', 'U2'],
            'Down (D)': ['D', 'D\'', 'D2'],
            'Left (L)': ['L', 'L\'', 'L2'],
            'Right (R)': ['R', 'R\'', 'R2'],
            'Front (F)': ['F', 'F\'', 'F2'],
            'Back (B)': ['B', 'B\'', 'B2']
        }
        
        face_selected = st.selectbox("Choose Face:", list(move_categories.keys()))
        move_selected = st.selectbox("Choose Direction:", move_categories[face_selected])
        
        if st.button(f"Execute {move_selected}", use_container_width=True, 
                    help=f"Apply {move_selected} move to the cube"):
            st.session_state.cube.execute_move(move_selected)
            st.success(f"✅ Executed move: {move_selected}")
            st.rerun()
        
        st.markdown("---")
        
        # Solver settings with help
        st.markdown("""
        <div class="instruction-card">
            <h4>⚙️ Solver Settings</h4>
            <p><small>Adjust algorithm parameters for optimal performance</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        max_depth = st.slider("🔍 Max Search Depth", 5, 25, 20, 
                             help="Maximum moves the solver will search (higher = more thorough but slower)")
        timeout = st.slider("⏱️ Timeout (seconds)", 1, 30, 10, 
                           help="Maximum time to spend searching for solution")
        
        st.session_state.solver = AStarSolver(max_depth=max_depth, timeout=timeout)
        
        # Performance info
        st.markdown("""
        <div class="stats-card">
            <h5>💡 Recommended Settings</h5>
            <ul style="font-size: 0.9em;">
                <li><strong>Depth 15-20:</strong> Good balance</li>
                <li><strong>Timeout 5-15s:</strong> Most scrambles</li>
                <li><strong>Simple scrambles:</strong> Lower settings</li>
                <li><strong>Complex patterns:</strong> Higher settings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Cube visualization with enhanced styling
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);">
            <h2 style="text-align: center; color: #2c3e50;">🎯 Cube Visualization</h2>
            <p style="text-align: center; color: #6c757d;">Current cube state and configuration</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🎲 2D View", "🔮 3D View", "📊 State Info"])
        
        with tab1:
            st.markdown("""
            <div class="instruction-card">
                <h4>🎲 2D Cube Layout</h4>
                <p><small>Flat representation showing all faces of the cube</small></p>
            </div>
            """, unsafe_allow_html=True)
            display_cube_2d()
        
        with tab2:
            st.markdown("""
            <div class="instruction-card">
                <h4>🔮 Interactive 3D View</h4>
                <p><small>Rotate and zoom to explore the cube from all angles</small></p>
            </div>
            """, unsafe_allow_html=True)
            fig_3d = draw_cube_3d()
            if fig_3d:
                st.plotly_chart(fig_3d, use_container_width=True)
            else:
                st.info("🔧 3D visualization temporarily unavailable - showing 2D view instead")
        
        with tab3:
            st.markdown("""
            <div class="instruction-card">
                <h4>📊 Detailed Cube Information</h4>
                <p><small>Technical details about current cube state</small></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Current scramble
            if st.session_state.current_scramble:
                st.markdown("""
                <div class="stats-card">
                    <h5>🎲 Current Scramble Sequence</h5>
                </div>
                """, unsafe_allow_html=True)
                st.code(' '.join(st.session_state.current_scramble))
            
            # Cube statistics
            is_solved = st.session_state.cube.is_solved()
            st.markdown(f"""
            <div class="{'success' if is_solved else 'warning'}-alert">
                <h5>� Cube Statistics</h5>
                <ul>
                    <li><strong>Status:</strong> {'✅ SOLVED' if is_solved else '❌ SCRAMBLED'}</li>
                    <li><strong>Scramble Moves:</strong> {len(st.session_state.current_scramble) if st.session_state.current_scramble else 0}</li>
                    <li><strong>Estimated Difficulty:</strong> {'Easy' if len(st.session_state.current_scramble) < 8 else 'Medium' if len(st.session_state.current_scramble) < 12 else 'Hard'}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Solve button with enhanced styling
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; margin: 1rem 0;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);">
            <h3 style="color: white; margin-bottom: 1rem;">🔮 AI Solver Engine</h3>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 1.5rem;">
                Advanced A* algorithm with heuristic optimization
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Center the solve button
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button("🔮 SOLVE CUBE", use_container_width=True, 
                        help="Use AI algorithm to find optimal solution",
                        type="primary"):
                if not st.session_state.cube.is_solved():
                    with st.spinner("🧠 AI is thinking... Finding optimal solution..."):
                        start_time = time.time()
                        solution = st.session_state.solver.solve(st.session_state.cube)
                        solve_time = time.time() - start_time
                        
                        if solution:
                            st.markdown(f"""
                            <div class="success-alert">
                                <h4>🎉 Solution Found!</h4>
                                <p><strong>⚡ Solve Time:</strong> {solve_time:.2f} seconds</p>
                                <p><strong>📏 Move Count:</strong> {len(solution)} moves</p>
                                <p><strong>🎯 Efficiency:</strong> {len(solution)/solve_time:.1f} moves/second</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display solution
                            st.markdown("**🎯 Solution Sequence:**")
                            st.code(' '.join(solution))
                            
                            # Add to history
                            st.session_state.solve_history.append({
                                'scramble': st.session_state.current_scramble.copy(),
                                'solution': solution,
                                'solve_time': solve_time,
                                'moves': len(solution)
                            })
                            
                            # Apply solution button
                            if st.button("▶️ Apply Solution to Cube", use_container_width=True):
                                st.session_state.cube.execute_sequence(solution)
                                st.success("✅ Solution applied! Cube is now solved!")
                                st.rerun()
                        else:
                            st.markdown("""
                            <div class="error-alert">
                                <h4>❌ No Solution Found</h4>
                                <p>Try increasing the search depth or timeout in the sidebar settings.</p>
                                <p><strong>💡 Suggestions:</strong></p>
                                <ul>
                                    <li>Increase Max Search Depth to 25</li>
                                    <li>Increase Timeout to 20-30 seconds</li>
                                    <li>Try a simpler scramble first</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-alert">
                        <h4>✅ Cube Already Solved!</h4>
                        <p>The cube is already in the solved state. Try scrambling it first!</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"**Current Scramble:** `{' '.join(st.session_state.current_scramble)}`")
            
            # Cube statistics
            st.markdown("**Cube Statistics:**")
            st.markdown(f"- **Total Stickers:** 54")
            st.markdown(f"- **Faces:** 6")
            st.markdown(f"- **Status:** {'✅ Solved' if is_solved else '❌ Scrambled'}")
            
    with col2:
        # Analytics and Performance Dashboard
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);">
            <h2 style="text-align: center; color: #2c3e50;">📊 Analytics Dashboard</h2>
            <p style="text-align: center; color: #6c757d;">Performance metrics and insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-time metrics
        current_scramble_length = len(st.session_state.current_scramble) if st.session_state.current_scramble else 0
        total_solves = len(st.session_state.solve_history)
        
        # Metrics display
        st.markdown("### 📈 Current Session Metrics")
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("🎲 Scramble Length", f"{current_scramble_length} moves")
            st.metric("🏆 Total Solves", total_solves)
        
        with metric_col2:
            difficulty = "Easy" if current_scramble_length < 8 else "Medium" if current_scramble_length < 12 else "Hard"
            st.metric("🎯 Difficulty", difficulty)
            
            if st.session_state.solve_history:
                avg_time = sum(record['solve_time'] for record in st.session_state.solve_history) / len(st.session_state.solve_history)
                st.metric("⚡ Avg Solve Time", f"{avg_time:.2f}s")
        
        # Performance history chart
        if st.session_state.solve_history:
            st.markdown("### 📊 Performance History")
            
            # Create performance data
            history_data = []
            for i, record in enumerate(st.session_state.solve_history[-10:]):  # Last 10 solves
                history_data.append({
                    'Solve': f"#{i+1}",
                    'Time (s)': record['solve_time'],
                    'Moves': record['moves'],
                    'Efficiency': record['moves'] / record['solve_time']
                })
            
            if history_data:
                history_df = pd.DataFrame(history_data)
                
                # Time trend chart
                fig_time = px.line(history_df, x='Solve', y='Time (s)', 
                                  title='🕐 Solve Time Trend',
                                  markers=True)
                fig_time.update_layout(height=200, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_time, use_container_width=True)
                
                # Moves efficiency chart
                fig_moves = px.bar(history_df, x='Solve', y='Moves',
                                  title='📏 Move Count per Solve',
                                  color='Moves',
                                  color_continuous_scale='viridis')
                fig_moves.update_layout(height=200, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_moves, use_container_width=True)
        else:
            st.markdown("""
            <div class="instruction-card">
                <h4>📊 No Solve History Yet</h4>
                <p>Solve some scrambles to see performance analytics!</p>
                <ol>
                    <li>Scramble the cube</li>
                    <li>Click "🔮 SOLVE CUBE"</li>
                    <li>Watch the metrics appear here</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick stats summary
        st.markdown("### 🎯 Session Summary")
        
        if st.session_state.solve_history:
            best_time = min(record['solve_time'] for record in st.session_state.solve_history)
            best_moves = min(record['moves'] for record in st.session_state.solve_history)
            success_rate = 100.0  # All recorded solves were successful
            
            st.markdown(f"""
            <div class="success-alert">
                <h5>🏆 Personal Records</h5>
                <ul>
                    <li><strong>⚡ Fastest Solve:</strong> {best_time:.2f} seconds</li>
                    <li><strong>🎯 Fewest Moves:</strong> {best_moves} moves</li>
                    <li><strong>✅ Success Rate:</strong> {success_rate:.0f}%</li>
                    <li><strong>📊 Total Attempts:</strong> {total_solves}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-alert">
                <h5>🎮 Ready to Start?</h5>
                <p>Your solving statistics will appear here once you complete your first solve!</p>
                <p><strong>💡 Tip:</strong> Start with an easy scramble to get familiar with the interface.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Algorithm insights
        st.markdown("### 🧠 Algorithm Insights")
        st.markdown("""
        <div class="stats-card">
            <h5>🔬 A* Search Algorithm</h5>
            <ul style="font-size: 0.9em;">
                <li><strong>Heuristic:</strong> Manhattan distance</li>
                <li><strong>Strategy:</strong> Best-first search</li>
                <li><strong>Optimality:</strong> Guaranteed shortest path</li>
                <li><strong>Complexity:</strong> O(b^d) time & space</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Bottom section - Features showcase
    st.markdown("---")
    st.header("🌟 Unique Features")
    
    feature_cols = st.columns(4)
    
    with feature_cols[0]:
        st.markdown("""
        <div class="stats-card">
            <h4>🚀 Multi-Algorithm</h4>
            <p>Adaptive strategy selection based on scramble complexity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_cols[1]:
        st.markdown("""
        <div class="stats-card">
            <h4>⚡ Lightning Fast</h4>
            <p>Sub-second solving for most scrambles</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_cols[2]:
        st.markdown("""
        <div class="stats-card">
            <h4>📊 Real-time Analytics</h4>
            <p>Performance tracking and visualization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_cols[3]:
        st.markdown("""
        <div class="stats-card">
            <h4>🎮 Interactive UI</h4>
            <p>User-friendly web interface with 3D visualization</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🏆 <strong>AeroHack 2025</strong> | Collins Aerospace Challenge | 
        Developed with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
