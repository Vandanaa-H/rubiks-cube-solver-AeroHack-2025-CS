"""
Console Interface for Rubik's Cube Solver
Provides interactive command-line interface for the solver.
"""

import os
import sys
from typing import List, Optional
from colorama import init, Fore, Style, Back

from ..core.cube import RubikCube
from ..algorithms.astar_solver import AStarSolver
from ..algorithms.utils import format_move_sequence, analyze_move_sequence

# Initialize colorama for Windows
init(autoreset=True)

class ConsoleInterface:
    """
    Interactive console interface for the Rubik's Cube Solver.
    """
    
    def __init__(self, cube: RubikCube, solver: AStarSolver):
        """Initialize the console interface."""
        self.cube = cube
        self.solver = solver
        self.running = True
        
    def run(self) -> None:
        """Main interface loop."""
        self.display_welcome()
        
        while self.running:
            self.display_menu()
            choice = input(f"\n{Fore.CYAN}Enter your choice: {Style.RESET_ALL}").strip()
            
            try:
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
            
            if self.running:
                input(f"\n{Fore.GREEN}Press Enter to continue...{Style.RESET_ALL}")
                self.clear_screen()
    
    def display_welcome(self) -> None:
        """Display welcome message."""
        self.clear_screen()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}")
        print("╔" + "═" * 60 + "╗")
        print("║" + " " * 15 + "RUBIK'S CUBE SOLVER" + " " * 15 + "║")
        print("║" + " " * 12 + "AeroHack 2025 - Collins Aerospace" + " " * 12 + "║")
        print("║" + " " * 60 + "║")
        print("║" + " " * 8 + "Algorithmic Puzzle Solving Challenge" + " " * 8 + "║")
        print("╚" + "═" * 60 + "╝")
        print(f"{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}Welcome to the interactive Rubik's Cube Solver!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}This solver uses A* search algorithm with advanced heuristics.{Style.RESET_ALL}\n")
    
    def display_menu(self) -> None:
        """Display main menu options."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}╔═══ MAIN MENU ═══╗{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. {Fore.GREEN}View Current Cube State{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. {Fore.GREEN}Scramble Cube{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. {Fore.GREEN}Solve Cube{Style.RESET_ALL}")
        print(f"{Fore.WHITE}4. {Fore.GREEN}Execute Manual Moves{Style.RESET_ALL}")
        print(f"{Fore.WHITE}5. {Fore.GREEN}Reset to Solved State{Style.RESET_ALL}")
        print(f"{Fore.WHITE}6. {Fore.GREEN}Load Scramble from File{Style.RESET_ALL}")
        print(f"{Fore.WHITE}7. {Fore.GREEN}Performance Test{Style.RESET_ALL}")
        print(f"{Fore.WHITE}8. {Fore.GREEN}Solver Settings{Style.RESET_ALL}")
        print(f"{Fore.WHITE}9. {Fore.GREEN}Help & Instructions{Style.RESET_ALL}")
        print(f"{Fore.WHITE}0. {Fore.RED}Exit{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╚" + "═" * 17 + "╝{Style.RESET_ALL}")
    
    def handle_choice(self, choice: str) -> None:
        """Handle user menu choice."""
        if choice == '1':
            self.view_cube_state()
        elif choice == '2':
            self.scramble_cube()
        elif choice == '3':
            self.solve_cube()
        elif choice == '4':
            self.manual_moves()
        elif choice == '5':
            self.reset_cube()
        elif choice == '6':
            self.load_scramble()
        elif choice == '7':
            self.performance_test()
        elif choice == '8':
            self.solver_settings()
        elif choice == '9':
            self.show_help()
        elif choice == '0':
            self.exit_program()
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
    
    def view_cube_state(self) -> None:
        """Display current cube state."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ CURRENT CUBE STATE ═══{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Cube Status: {self.get_cube_status()}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Moves Made: {self.cube.get_move_count()}{Style.RESET_ALL}")
        
        if self.cube.move_history:
            print(f"\n{Fore.CYAN}Move History:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{format_move_sequence(self.cube.move_history)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Cube Visualization:{Style.RESET_ALL}")
        self.display_cube_visual()
    
    def get_cube_status(self) -> str:
        """Get colored cube status."""
        if self.cube.is_solved():
            return f"{Fore.GREEN}{Style.BRIGHT}SOLVED ✓{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}{Style.BRIGHT}SCRAMBLED{Style.RESET_ALL}"
    
    def display_cube_visual(self) -> None:
        """Display visual representation of the cube."""
        print(f"\n{Fore.WHITE}Visual representation:{Style.RESET_ALL}")
        print(self.cube)
    
    def scramble_cube(self) -> None:
        """Scramble the cube with user input."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ SCRAMBLE CUBE ═══{Style.RESET_ALL}")
        
        try:
            num_moves = int(input(f"{Fore.CYAN}Number of scramble moves (default 20): {Style.RESET_ALL}") or "20")
            if num_moves < 1 or num_moves > 100:
                print(f"{Fore.RED}Invalid number. Using default (20).{Style.RESET_ALL}")
                num_moves = 20
            
            print(f"\n{Fore.YELLOW}Scrambling cube with {num_moves} moves...{Style.RESET_ALL}")
            
            scramble_moves = self.cube.scramble(num_moves)
            
            print(f"{Fore.GREEN}✓ Cube scrambled successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Scramble sequence:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{format_move_sequence(scramble_moves)}{Style.RESET_ALL}")
            
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
    
    def solve_cube(self) -> None:
        """Solve the current cube state."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ SOLVE CUBE ═══{Style.RESET_ALL}")
        
        if self.cube.is_solved():
            print(f"{Fore.GREEN}Cube is already solved! ✓{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Analyzing cube state...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Starting A* search algorithm...{Style.RESET_ALL}")
        print(f"{Fore.WHITE}(This may take a few moments for complex scrambles){Style.RESET_ALL}")
        
        try:
            solution = self.solver.solve(self.cube.copy())
            
            if solution:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ SOLUTION FOUND!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Solution length: {Fore.WHITE}{len(solution)} moves{Style.RESET_ALL}")
                print(f"\n{Fore.CYAN}Solution sequence:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{format_move_sequence(solution)}{Style.RESET_ALL}")
                
                # Show statistics
                stats = self.solver.get_statistics()
                print(f"\n{Fore.YELLOW}Search Statistics:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{stats}{Style.RESET_ALL}")
                
                # Ask if user wants to apply solution
                apply = input(f"\n{Fore.CYAN}Apply solution to cube? (y/n): {Style.RESET_ALL}").lower()
                if apply in ['y', 'yes']:
                    self.cube.execute_sequence(solution)
                    print(f"{Fore.GREEN}✓ Solution applied! Cube is now solved.{Style.RESET_ALL}")
                
            else:
                print(f"\n{Fore.RED}❌ No solution found within constraints.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Try increasing the search depth or timeout in settings.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"\n{Fore.RED}Error during solving: {e}{Style.RESET_ALL}")
    
    def manual_moves(self) -> None:
        """Allow user to input manual moves."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ MANUAL MOVES ═══{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Valid moves: U, U', U2, D, D', D2, L, L', L2, R, R', R2, F, F', F2, B, B', B2{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Enter moves separated by spaces, or 'back' to undo last move{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Example: U R U' R' F R F'{Style.RESET_ALL}")
        
        move_input = input(f"\n{Fore.CYAN}Enter moves: {Style.RESET_ALL}").strip()
        
        if not move_input:
            return
        
        if move_input.lower() == 'back':
            if self.cube.move_history:
                last_move = self.cube.move_history[-1]
                print(f"{Fore.YELLOW}Undoing last move: {last_move}{Style.RESET_ALL}")
                # This would require implementing undo functionality
                print(f"{Fore.RED}Undo functionality not implemented yet.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No moves to undo.{Style.RESET_ALL}")
            return
        
        try:
            moves = move_input.split()
            invalid_moves = [m for m in moves if not self.cube.move_engine.is_valid_move(m)]
            
            if invalid_moves:
                print(f"{Fore.RED}Invalid moves: {', '.join(invalid_moves)}{Style.RESET_ALL}")
                return
            
            print(f"{Fore.YELLOW}Executing {len(moves)} moves...{Style.RESET_ALL}")
            self.cube.execute_sequence(moves)
            print(f"{Fore.GREEN}✓ Moves executed successfully!{Style.RESET_ALL}")
            
            # Show updated status
            print(f"\n{Fore.WHITE}New status: {self.get_cube_status()}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}Error executing moves: {e}{Style.RESET_ALL}")
    
    def reset_cube(self) -> None:
        """Reset cube to solved state."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ RESET CUBE ═══{Style.RESET_ALL}")
        
        confirm = input(f"{Fore.CYAN}Reset cube to solved state? (y/n): {Style.RESET_ALL}").lower()
        if confirm in ['y', 'yes']:
            self.cube.reset()
            print(f"{Fore.GREEN}✓ Cube reset to solved state!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Reset cancelled.{Style.RESET_ALL}")
    
    def load_scramble(self) -> None:
        """Load scramble from file."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ LOAD SCRAMBLE ═══{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Available scramble files:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Easy scrambles{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Medium scrambles{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Hard scrambles{Style.RESET_ALL}")
        print(f"{Fore.WHITE}4. Custom file{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Choose option (1-4): {Style.RESET_ALL}").strip()
        
        file_map = {
            '1': 'assets/cube_states/easy_scrambles.txt',
            '2': 'assets/cube_states/medium_scrambles.txt',
            '3': 'assets/cube_states/hard_scrambles.txt'
        }
        
        if choice in file_map:
            filename = file_map[choice]
            try:
                with open(filename, 'r') as f:
                    scrambles = [line.strip() for line in f if line.strip()]
                
                if scrambles:
                    print(f"\n{Fore.CYAN}Found {len(scrambles)} scrambles. Select one:{Style.RESET_ALL}")
                    for i, scramble in enumerate(scrambles[:10], 1):  # Show first 10
                        print(f"{Fore.WHITE}{i}. {scramble[:50]}{'...' if len(scramble) > 50 else ''}{Style.RESET_ALL}")
                    
                    idx = int(input(f"\n{Fore.CYAN}Enter number (1-{min(len(scrambles), 10)}): {Style.RESET_ALL}")) - 1
                    if 0 <= idx < len(scrambles):
                        moves = scrambles[idx].split()
                        self.cube.reset()
                        self.cube.execute_sequence(moves)
                        print(f"{Fore.GREEN}✓ Scramble loaded successfully!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}No scrambles found in file.{Style.RESET_ALL}")
                    
            except FileNotFoundError:
                print(f"{Fore.RED}File not found: {filename}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error loading file: {e}{Style.RESET_ALL}")
        
        elif choice == '4':
            filename = input(f"{Fore.CYAN}Enter custom file path: {Style.RESET_ALL}").strip()
            print(f"{Fore.YELLOW}Custom file loading not implemented yet.{Style.RESET_ALL}")
        
        else:
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
    
    def performance_test(self) -> None:
        """Run performance tests."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ PERFORMANCE TEST ═══{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Running performance benchmark...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}This will test the solver on multiple scrambles.{Style.RESET_ALL}")
        
        num_tests = int(input(f"\n{Fore.CYAN}Number of test scrambles (default 5): {Style.RESET_ALL}") or "5")
        
        successful_solves = 0
        total_time = 0
        total_moves = 0
        
        for i in range(num_tests):
            print(f"\n{Fore.WHITE}Test {i+1}/{num_tests}:{Style.RESET_ALL}")
            
            # Create test scramble
            test_cube = RubikCube()
            scramble_moves = test_cube.scramble(20, seed=i)
            print(f"{Fore.CYAN}Scramble: {' '.join(scramble_moves[:10])}{'...' if len(scramble_moves) > 10 else ''}{Style.RESET_ALL}")
            
            # Solve
            solution = self.solver.solve(test_cube)
            stats = self.solver.get_statistics()
            
            if solution:
                successful_solves += 1
                total_time += stats.solve_time
                total_moves += len(solution)
                print(f"{Fore.GREEN}✓ Solved in {stats.solve_time:.2f}s, {len(solution)} moves{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Failed to solve{Style.RESET_ALL}")
        
        # Show results
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ RESULTS ═══{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Success rate: {successful_solves}/{num_tests} ({100*successful_solves/num_tests:.1f}%){Style.RESET_ALL}")
        if successful_solves > 0:
            print(f"{Fore.WHITE}Average solve time: {total_time/successful_solves:.2f}s{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Average solution length: {total_moves/successful_solves:.1f} moves{Style.RESET_ALL}")
    
    def solver_settings(self) -> None:
        """Configure solver settings."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ SOLVER SETTINGS ═══{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Current settings:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Max depth: {Fore.WHITE}{self.solver.max_depth}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Timeout: {Fore.WHITE}{self.solver.timeout}s{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}1. Change max depth{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Change timeout{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Reset to defaults{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Choose option (1-3): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            try:
                new_depth = int(input(f"{Fore.CYAN}New max depth (current: {self.solver.max_depth}): {Style.RESET_ALL}"))
                if 1 <= new_depth <= 50:
                    self.solver.max_depth = new_depth
                    print(f"{Fore.GREEN}✓ Max depth updated to {new_depth}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid depth. Must be between 1 and 50.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input.{Style.RESET_ALL}")
        
        elif choice == '2':
            try:
                new_timeout = float(input(f"{Fore.CYAN}New timeout in seconds (current: {self.solver.timeout}): {Style.RESET_ALL}"))
                if 1 <= new_timeout <= 300:
                    self.solver.timeout = new_timeout
                    print(f"{Fore.GREEN}✓ Timeout updated to {new_timeout}s{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid timeout. Must be between 1 and 300 seconds.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input.{Style.RESET_ALL}")
        
        elif choice == '3':
            self.solver.max_depth = 25
            self.solver.timeout = 60.0
            print(f"{Fore.GREEN}✓ Settings reset to defaults{Style.RESET_ALL}")
    
    def show_help(self) -> None:
        """Display help and instructions."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}═══ HELP & INSTRUCTIONS ═══{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}RUBIK'S CUBE NOTATION:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}U, D, L, R, F, B = Clockwise 90° rotation of face{Style.RESET_ALL}")
        print(f"{Fore.WHITE}U', D', L', R', F', B' = Counterclockwise 90° rotation{Style.RESET_ALL}")
        print(f"{Fore.WHITE}U2, D2, L2, R2, F2, B2 = 180° rotation{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}FACE MEANINGS:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}U = Up (top face){Style.RESET_ALL}")
        print(f"{Fore.WHITE}D = Down (bottom face){Style.RESET_ALL}")
        print(f"{Fore.WHITE}L = Left face{Style.RESET_ALL}")
        print(f"{Fore.WHITE}R = Right face{Style.RESET_ALL}")
        print(f"{Fore.WHITE}F = Front face{Style.RESET_ALL}")
        print(f"{Fore.WHITE}B = Back face{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}ALGORITHM INFORMATION:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}• Uses A* search with corner-edge heuristic{Style.RESET_ALL}")
        print(f"{Fore.WHITE}• Optimal solutions for scrambles up to 20 moves{Style.RESET_ALL}")
        print(f"{Fore.WHITE}• Search can be customized via settings menu{Style.RESET_ALL}")
        print(f"{Fore.WHITE}• Performance depends on scramble complexity{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}TIPS:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}• Start with easy scrambles (≤15 moves){Style.RESET_ALL}")
        print(f"{Fore.WHITE}• Increase timeout for complex scrambles{Style.RESET_ALL}")
        print(f"{Fore.WHITE}• Use performance test to evaluate settings{Style.RESET_ALL}")
    
    def exit_program(self) -> None:
        """Exit the program."""
        print(f"\n{Fore.YELLOW}Thank you for using the Rubik's Cube Solver!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}AeroHack 2025 - Collins Aerospace{Style.RESET_ALL}")
        self.running = False
    
    def clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')