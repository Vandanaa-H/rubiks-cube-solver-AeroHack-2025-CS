"""
Test runner for the Rubik's Cube Solver
Comprehensive testing suite with reporting and coverage.
"""

import sys
import os
import time
import subprocess
from pathlib import Path


# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        end_time = time.time()
        
        print(f"\n📊 Results:")
        print(f"Exit code: {result.returncode}")
        print(f"Duration: {end_time - start_time:.2f}s")
        
        if result.stdout:
            print(f"\n📋 Output:")
            print(result.stdout)
        
        if result.stderr:
            print(f"\n⚠️  Errors:")
            print(result.stderr)
        
        success = result.returncode == 0
        print(f"\n{'✅ PASSED' if success else '❌ FAILED'}")
        return success
        
    except subprocess.TimeoutExpired:
        print(f"\n⏰ TIMEOUT (300s)")
        return False
    except Exception as e:
        print(f"\n💥 EXCEPTION: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 CHECKING DEPENDENCIES")
    print("="*40)
    
    required_packages = [
        'numpy', 'matplotlib', 'colorama', 'pytest'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("\n✅ All dependencies satisfied")
    return True

def run_unit_tests():
    """Run unit tests using pytest."""
    return run_command(
        ['python', '-m', 'pytest', 'src/tests/', '-v', '--tb=short'],
        "UNIT TESTS"
    )

def run_integration_tests():
    """Run integration tests."""
    return run_command(
        ['python', '-m', 'pytest', 'src/tests/test_integration.py', '-v'],
        "INTEGRATION TESTS"
    )

def run_performance_tests():
    """Run performance benchmarks."""
    return run_command(
        ['python', 'examples/performance_test.py'],
        "PERFORMANCE TESTS"
    )

def run_basic_examples():
    """Run basic usage examples."""
    return run_command(
        ['python', 'examples/basic_usage.py'],
        "BASIC USAGE EXAMPLES"
    )

def test_import_structure():
    """Test that all modules can be imported correctly."""
    print("\n🔍 TESTING IMPORT STRUCTURE")
    print("="*40)
    
    modules_to_test = [
        'src.core.cube',
        'src.core.moves',
        'src.algorithms.astar_solver',
        'src.algorithms.heuristics',
        'src.algorithms.utils',
        'src.ui.console_interface',
        'src.ui.visualizer'
    ]
    
    all_success = True
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except Exception as e:
            print(f"❌ {module}: {e}")
            all_success = False
    
    return all_success

def test_basic_functionality():
    """Test basic functionality without pytest."""
    print("\n🎯 TESTING BASIC FUNCTIONALITY")
    print("="*40)
    
    try:
        # Test cube creation and basic operations
        from src.core.cube import RubikCube
        
        cube = RubikCube()
        print("✅ Cube creation")
        
        assert cube.is_solved(), "Cube should start solved"
        print("✅ Initial solved state")
        
        cube.execute_move('U')
        assert not cube.is_solved(), "Cube should not be solved after move"
        print("✅ Move execution")
        
        cube.reset()
        assert cube.is_solved(), "Cube should be solved after reset"
        print("✅ Cube reset")
        
        # Test solver
        from src.algorithms.astar_solver import AStarSolver
        
        solver = AStarSolver(max_depth=10, timeout=5)
        print("✅ Solver creation")
        
        cube.execute_sequence(['U', 'R'])
        solution = solver.solve(cube.copy())
        assert solution is not None, "Should find solution for simple scramble"
        print("✅ Basic solving")
        
        # Test visualization
        from src.ui.visualizer import CubeVisualizer
        
        visualizer = CubeVisualizer()
        ascii_art = visualizer.display_ascii_art(cube)
        assert isinstance(ascii_art, str), "Should return string"
        assert len(ascii_art) > 0, "Should not be empty"
        print("✅ Visualization")
        
        print("\n✅ ALL BASIC FUNCTIONALITY TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ BASIC FUNCTIONALITY TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_test_report(results):
    """Generate a comprehensive test report."""
    print("\n" + "="*80)
    print("📋 COMPREHENSIVE TEST REPORT")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"\n📊 Summary:")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success rate: {100 * passed_tests / total_tests:.1f}%")
    
    print(f"\n📋 Detailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    overall_success = all(results.values())
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 Congratulations! Your Rubik's Cube Solver is working perfectly!")
        print("You can now run the main application with: python main.py")
    else:
        print("\n🔧 Some tests failed. Please check the output above for details.")
        print("Make sure all dependencies are installed and try again.")
    
    return overall_success

def main():
    """Main test runner function."""
    print("🎯 RUBIK'S CUBE SOLVER - COMPREHENSIVE TEST SUITE")
    print("AeroHack 2025 - Collins Aerospace")
    print("Author: Ullas Vandana")
    print("=" * 80)
    
    start_time = time.time()
    
    # Check if we're in the right directory
    if not os.path.exists('src') or not os.path.exists('main.py'):
        print("❌ Please run this script from the project root directory")
        print("Expected structure: src/, main.py, requirements.txt")
        return False
    
    # Dictionary to store test results
    test_results = {}
    
    # Check dependencies first
    print("\n🔧 DEPENDENCY CHECK")
    test_results["Dependencies"] = check_dependencies()
    
    if not test_results["Dependencies"]:
        print("\n❌ Cannot proceed without required dependencies")
        return False
    
    # Test import structure
    test_results["Import Structure"] = test_import_structure()
    
    # Test basic functionality
    test_results["Basic Functionality"] = test_basic_functionality()
    
    # Run pytest-based tests
    test_results["Unit Tests"] = run_unit_tests()
    test_results["Integration Tests"] = run_integration_tests()
    
    # Run examples and performance tests
    test_results["Basic Examples"] = run_basic_examples()
    test_results["Performance Tests"] = run_performance_tests()
    
    # Generate final report
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n⏱️  Total testing time: {total_time:.1f} seconds")
    
    overall_success = generate_test_report(test_results)
    
    return overall_success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)